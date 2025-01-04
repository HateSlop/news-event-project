import streamlit as st
import pandas as pd
from db_manager import fetch_data
from main_pipeline import companies

# 사이드바: 필터링 옵션 추가
st.sidebar.title("필터 옵션")
filter_option = st.sidebar.selectbox(
    "회사 선택",
    companies,  # 기업 리스트
    index=0
)

# 데이터 불러오기 및 필터링
data = fetch_data(company=filter_option)  # 선택된 회사 데이터 불러오기

if not data.empty:
    # 1. 메인 테이블: 날짜, 카테고리, 주요 이벤트만 표시
    st.title(f"{filter_option} 데이터 시각화")
    st.write("### 메인 테이블")
    main_table = data[["날짜", "문서 카테고리", "주요 이벤트"]]
    st.dataframe(main_table)

    # 2. 요약 보기 옵션
    show_summary = st.checkbox("요약 보기")
    if show_summary:
        st.write("### 요약 내용")
        for _, row in data.iterrows():
            st.write(f"**날짜**: {row['날짜']}")
            if row["문서 카테고리"]:
                st.write(f"**카테고리**: {row['문서 카테고리']}")
            st.write(f"**요약 내용**: {row['요약']}")
            st.write("---")  # 구분선
else:
    st.warning(f"{filter_option}에 해당하는 데이터가 없습니다.")
