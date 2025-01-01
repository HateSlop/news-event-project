import streamlit as st
import pandas as pd
import json
from db_manager import fetch_data

# 사이드바 필터
st.sidebar.title("필터 옵션")
filter_option = st.sidebar.selectbox("회사 선택", ["Nvidia", "Apple", "Tesla"], index=0)
start_date = st.sidebar.date_input("시작 날짜", value=pd.to_datetime("2024-01-01"))
end_date   = st.sidebar.date_input("종료 날짜", value=pd.to_datetime("2024-05-10"))

# DB에서 데이터 불러오기
data = fetch_data(company=filter_option)

# 날짜 변환
data["date"] = pd.to_datetime(data["date"], errors="coerce")
mask = (data["date"] >= pd.to_datetime(start_date)) & (data["date"] <= pd.to_datetime(end_date))
data = data[mask]

# 메인 타이틀
st.title(f"{filter_option} 데이터 시각화")

# ── 메인 테이블 ─────────────────────────────────
st.write("### 메인 테이블")
main_table = data[["date", "문서 카테고리", "주요 이벤트"]].reset_index(drop=True)
st.dataframe(main_table)

# ── 요약 내용 ──────────────────────────────────
st.write("### 요약 내용")

for _, row in data.iterrows():
    date_val = row["date"]
    category_val = row["문서 카테고리"]
    val = row["요약"]

    if isinstance(val, str) and val.strip():
        parsed_json = json.loads(val)
        cat_in_json = parsed_json["문서 카테고리"]
        events_in_json = parsed_json["주요 이벤트"]
        summary_in_json = parsed_json["요약"]

        date_str = date_val.strftime("%Y-%m-%d") if pd.notnull(date_val) else "N/A"

        st.write(f"**날짜**: {date_str}")
        st.write(f"**카테고리**: {cat_in_json}")
        st.write(f"**주요 이벤트**: {events_in_json}")
        st.write(f"**요약 내용**: {summary_in_json}")
        st.write("---")
    else:
        st.write(f"**날짜**: {date_val if pd.notnull(date_val) else 'N/A'}")
        st.write(f"**카테고리**: {category_val}")
        st.write("**주요 이벤트**: (없음)")
        st.write("**요약 내용**: (없음)")
        st.write("---")
