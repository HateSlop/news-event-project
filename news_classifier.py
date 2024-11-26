import config
from langchain_openai import ChatOpenAI
from news_crawler import NewsCrawler
import json
from prompt_template import prompt, sentiment_prompt
from datetime import datetime
import pandas as pd

class NewsClassifier:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.sentiment_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            openai_api_key=config.OPENAI_API_KEY
        )
        
    def validate_news_data(self, df):
        """뉴스 데이터 검증"""
        required_columns = ['url', 'title', 'seendate', 'domain', 'language', 'sourcecountry']
        
        # 필수 컬럼 존재 여부 확인
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"필수 컬럼이 누락되었습니다: {missing_cols}")
            
        # 데이터 타입 검증
        if not pd.to_datetime(df['seendate'], errors='coerce').notna().all():
            raise ValueError("seendate 컬럼에 잘못된 날짜 형식이 있습니다")
            
        # URL 형식 검증
        if not df['url'].str.contains('^https?://', regex=True).all():
            raise ValueError("잘못된 URL 형식이 있습니다")
            
        # 빈 제목 확인
        if df['title'].isna().any():
            raise ValueError("제목이 없는 기사가 있습니다")
            
        return True

    def classify_news(self, text):
        """뉴스 텍스트를 분류하고 요약합니다."""
        try:
            # 입력 텍스트 검증
            if not text or len(text.strip()) == 0:
                raise ValueError("입력 텍스트가 비어있습니다")
                
            # 프롬프트 템플릿에 뉴스 텍스트 추가
            full_prompt = prompt + text
            
            # LLM으로 분류 및 요약 수행
            response = self.llm.invoke(full_prompt)
            
            # 응답을 문자열로 변환
            response_text = response.content
            if not response_text:
                raise ValueError("LLM 응답이 비어있습니다")
                
            # JSON 형식 검증 및 파싱
            try:
                # JSON 문자열 정제 전에 로깅 추가
                print("원본 응답:", response_text)
                
                if not response_text.strip().startswith('{'):
                    response_text = '{' + response_text.split('{', 1)[1]
                if not response_text.strip().endswith('}'):
                    response_text = response_text.rsplit('}', 1)[0] + '}'
                    
                # 정제된 JSON 문자열 로깅
                print("정제된 JSON:", response_text)
                
                result = json.loads(response_text)
            except (IndexError, json.JSONDecodeError) as e:
                raise ValueError(f"JSON 파싱 실패: {str(e)}")
            
            # 필수 필드 검증
            required_fields = ['문서 카테고리', '요약', '주요 이벤트']
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                raise ValueError(f"필수 필드 누락: {missing_fields}")
            
            # 감성분석 수행
            sentiment_full_prompt = sentiment_prompt + text
            sentiment_response = self.sentiment_llm.invoke(sentiment_full_prompt)
            
            # 감성분석 응답 처리
            sentiment_text = sentiment_response.content
            if not sentiment_text:
                raise ValueError("감성분석 응답이 비어있습니다")
                
            try:
                # 감성분석 JSON 파싱 전 로깅 추가
                print("감성분석 원본 응답:", sentiment_text)
                
                if not sentiment_text.strip().startswith('{'):
                    sentiment_text = '{' + sentiment_text.split('{', 1)[1]
                if not sentiment_text.strip().endswith('}'):
                    sentiment_text = sentiment_text.rsplit('}', 1)[0] + '}'
                    
                # 정제된 감성분석 JSON 로깅
                print("정제된 감성분석 JSON:", sentiment_text)
                
                sentiment_result = json.loads(sentiment_text)
            except (IndexError, json.JSONDecodeError) as e:
                raise ValueError(f"감성분석 JSON 파싱 실패: {str(e)}")
            
            # 감성분석 결과 추가
            result['감성분석'] = sentiment_result
            result['분석_날짜'] = datetime.now().strftime('%Y-%m-%d')
            
            return result
        except Exception as e:
            print(f"뉴스 분류 중 오류 발생: {str(e)}")
            return None
            
    def process_news_batch(self, df):
        """여러 뉴스를 분류합니다."""
        results = []
        
        try:
            # 데이터 검증
            self.validate_news_data(df)
            
            # 각 뉴스 분류 및 요약
            for _, row in df.iterrows():
                if pd.notna(row['title']):  # 제목이 있는 경우만 처리
                    result = self.classify_news(row['title'])
                    if result:
                        result['제목'] = row['title']
                        result['URL'] = row['url']
                        result['도메인'] = row['domain']
                        result['게시일'] = row['seendate']
                        results.append(result)
                    
        except Exception as e:
            print(f"뉴스 처리 중 오류 발생: {e}")
            
        return results

def main():
    # 뉴스 크롤러 초기화 및 데이터 수집
    crawler = NewsCrawler()
    keywords = ["Apple"] #"Tesla", "Microsoft", "Google", "Amazon", "Meta"
    articles_df = crawler.get_news_urls(keywords)
    
    if not articles_df.empty:
        # 뉴스 분류기 초기화 및 분류 수행
        classifier = NewsClassifier()
        results = classifier.process_news_batch(articles_df)
        
        # 결과 출력
        print(f"\n총 {len(results)}개의 뉴스가 처리되었습니다.")
        for result in results:
            print("\n=== 뉴스 분석 결과 ===")
            print(f"제목: {result['제목']}")
            print(f"URL: {result['URL']}")
            print(f"도메인: {result['도메인']}")
            print(f"게시일: {result['게시일']}")
            print(f"카테고리: {result['문서 카테고리']}")
            print(f"요약: {result['요약']}")
            print(f"주요 이벤트: {', '.join(result['주요 이벤트'])}")
            print(f"감성분석 결과: {result['감성분석']}")
            print(f"분석 날짜: {result['분석_날짜']}")

if __name__ == "__main__":
    main()
