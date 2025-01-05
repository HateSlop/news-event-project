import streamlit as st
import pandas as pd
from db_manager import fetch_data

# Streamlit 앱 제목
st.title("기업 뉴스 대시보드")

# 기업 선택 옵션
companies = ["Apple", "Microsoft", "Google", "Amazon"]
selected_company = st.sidebar.selectbox("기업명 선택", companies)

# 날짜 범위 선택
start_date = st.sidebar.date_input("시작 날짜", value=pd.Timestamp("2024-11-01"))
end_date = st.sidebar.date_input("종료 날짜", value=pd.Timestamp("2024-12-31"))

# 데이터 필터링
if st.sidebar.button("데이터 검색"):
    try:
        # 데이터베이스에서 데이터 가져오기
        news_data = fetch_data(selected_company, start_date, end_date)

        if news_data:
            # 데이터프레임 생성
            df = pd.DataFrame(news_data)
            df.columns = ["date", "title", "summary", "sentiment", "category", "events"]
            
            # 데이터 테이블 표시
            st.subheader(f"{selected_company}의 문서 목록")
            st.dataframe(df)

            # 개별 요약 보기
            show_summaries = st.checkbox("요약 보기")
            if show_summaries:
                for index, row in df.iterrows():
                    st.markdown(f"### {row['date']} - {row['title']}")
                    st.write(f"**요약:** {row['summary']}")
                    st.write(f"**감정 분석:** {row['sentiment']}")
        else:
            st.warning("선택한 조건에 맞는 데이터가 없습니다.")

    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류 발생: {e}")
