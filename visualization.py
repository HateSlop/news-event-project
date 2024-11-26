import streamlit as st
import pandas as pd
from db_manager import DBManager
import plotly.express as px
from datetime import datetime, timedelta
import config

class NewsVisualization:
    def __init__(self):
        try:
            self.db_manager = DBManager()
        except AttributeError as e:
            st.error("MongoDB 연결 설정이 필요합니다. config.py 파일에 MONGODB_URI를 추가해주세요.")
            st.stop()
    def run_dashboard(self):
        """Streamlit 대시보드를 실행합니다."""
        st.title("📰 뉴스 이벤트 대시보드")
        
        # 사이드바 - 카테고리 필터
        st.sidebar.header("필터")
        categories = ["전체", "정책/금융", "채권/외환", "IB/기업", "증권", "국제뉴스", "해외주식", "부동산"]
        selected_category = st.sidebar.selectbox("카테고리 선택", categories)
        
        # 최근 뉴스 데이터 조회
        if selected_category == "전체":
            news_data = self.db_manager.get_recent_news(100)
        else:
            news_data = self.db_manager.get_news_by_category(selected_category)
            
        if not news_data:
            st.warning("표시할 뉴스가 없습니다.")
            return
            
        # 데이터프레임 변환
        df = pd.DataFrame(news_data)
        
        # 1. 카테고리별 뉴스 분포
        st.header("📊 카테고리별 뉴스 분포")
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            fig_category = px.pie(values=category_counts.values, 
                                names=category_counts.index,
                                title="카테고리별 뉴스 비율")
            st.plotly_chart(fig_category)
        else:
            st.warning("카테고리 정보가 없습니다.")
        
        # 2. 기업별 감성분석 추이
        st.header("📈 기업별 감성분석 추이")
        
        # published_date 전처리
        def parse_datetime(date_str):
            try:
                if isinstance(date_str, str) and 'T' in date_str:
                    return datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')
                return pd.to_datetime(date_str)
            except:
                return pd.NaT

        df['published_date'] = df['published_date'].apply(parse_datetime)
        
        # 감성분석 데이터 추출 및 정리
        sentiment_data = []
        for _, row in df.iterrows():
            if pd.notna(row['published_date']):
                if 'sentiment' in row and isinstance(row['sentiment'], dict):
                    for company, score in row['sentiment'].items():
                        sentiment_data.append({
                            'date': row['published_date'],
                            'company': company,
                            'sentiment_score': score
                        })
        
        if sentiment_data:
            sentiment_df = pd.DataFrame(sentiment_data)
            
            # 같은 날짜와 기업에 대해 감성점수 평균 계산
            sentiment_df = sentiment_df.groupby(['date', 'company'])['sentiment_score'].mean().reset_index()
            
            # 날짜순으로 정렬
            sentiment_df = sentiment_df.sort_values('date')
            
            # 기업별 감성점수 추이 그래프
            fig_sentiment = px.line(sentiment_df,
                                  x='date',
                                  y='sentiment_score',
                                  color='company',
                                  title="기업별 감성점수 추이",
                                  markers=True)
            
            fig_sentiment.update_xaxes(
                title_text="뉴스 게시일",
                tickformat="%Y-%m-%d %H:%M",
                tickangle=45
            )
            
            fig_sentiment.update_yaxes(
                title_text="감성점수 (-5 ~ +5)"
            )
            
            st.plotly_chart(fig_sentiment)
        else:
            st.warning("감성분석 데이터가 없습니다.")
        # 3. 최근 뉴스 목록
        st.header("📑 최근 뉴스 목록")
        for idx, news in enumerate(news_data[:10]):
            with st.expander(f"{idx+1}. {news.get('title', '제목 없음')}"):
                published_date = news.get('published_date', '게시일 없음')
                if isinstance(published_date, str) and 'T' in published_date:
                    # ISO 형식 날짜를 한국 형식으로 변환
                    try:
                        date_obj = datetime.strptime(published_date, '%Y%m%dT%H%M%SZ')
                        formatted_date = date_obj.strftime('%Y년 %m월 %d일 %H:%M')
                        st.write(f"**게시일:** {formatted_date}")
                    except:
                        st.write(f"**게시일:** {published_date}")
                else:
                    st.write(f"**게시일:** {published_date}")
                st.write(f"**카테고리:** {news.get('category', '카테고리 없음')}")
                st.write(f"**요약:** {news.get('summary', '요약 없음')}")
                if 'events' in news:
                    st.write(f"**주요 이벤트:** {', '.join(news['events'])}")
                if 'sentiment' in news and isinstance(news['sentiment'], dict):
                    st.write("**감성분석 결과:**")
                    for company, score in news['sentiment'].items():
                        st.write(f"- {company}: {score}")

def main():
    viz = NewsVisualization()
    viz.run_dashboard()

if __name__ == "__main__":
    main()
