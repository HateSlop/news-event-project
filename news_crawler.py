import config
from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
from datetime import datetime, timedelta
import pandas as pd
import time

class NewsCrawler:
    def __init__(self):
        self.gdelt = GdeltDoc()
        
    def get_news_urls(self, keywords, days=7):
        """
        GDELT API를 사용하여 뉴스 URL을 수집합니다.
        
        Args:
            keywords (list): 검색할 키워드 리스트
            days (int): 현재 날짜로부터 검색할 이전 날짜 수
            
        Returns:
            pandas.DataFrame: 수집된 뉴스 정보가 담긴 데이터프레임
        """
        all_articles = pd.DataFrame()
        
        for keyword in keywords:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            filters = Filters(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                num_records=100,  # 각 키워드당 수집할 뉴스 수 조정
                keyword=keyword,
                country="US"  # 미국 뉴스로 한정
            )
            
            try:
                articles = self.gdelt.article_search(filters)
                if not articles.empty:
                    all_articles = pd.concat([all_articles, articles])
                print(f"'{keyword}' 키워드로 {len(articles)}개의 뉴스 수집 완료")
                time.sleep(1)  # API 호출 간 딜레이 추가
                
            except Exception as e:
                print(f"'{keyword}' 키워드 뉴스 수집 중 오류 발생: {e}")
                continue
                
        print(f"총 수집된 뉴스 개수: {len(all_articles)}")
        return all_articles.drop_duplicates(subset=['url'])
            
    def extract_article_content(self, articles_df):
        """
        수집된 URL에서 뉴스 본문을 추출합니다.
        
        Args:
            articles_df (pandas.DataFrame): 뉴스 URL이 포함된 데이터프레임
            
        Returns:
            list: 뉴스 본문 리스트
            list: 뉴스 제목 리스트
        """
        texts = []
        titles = []
        
        for idx, row in articles_df.iterrows():
            try:
                article = Article(row['url'])
                article.download()
                time.sleep(0.5)  # 다운로드 간 딜레이 추가
                article.parse()
                
                # 빈 본문이나 너무 짧은 본문은 제외
                if article.text and len(article.text.split()) > 50:
                    texts.append(article.text)
                    titles.append(article.title)
                    print(f"기사 {idx+1} 추출 완료 (길이: {len(article.text.split())} 단어)")
                else:
                    print(f"기사 {idx+1} 건너뜀: 본문이 너무 짧거나 비어있음")
                    continue
                
            except Exception as e:
                print(f"기사 {idx+1} 추출 실패: {e}")
                continue
                
        return texts, titles

def main():
    crawler = NewsCrawler()
    
    # 관심 키워드 설정 및 검색 기간 확장
    keywords = ["Apple", "Tesla", "Microsoft", "Google", "Amazon", "Meta"]
    
    # 뉴스 URL 수집
    articles_df = crawler.get_news_urls(keywords, days=14)  # 검색 기간 2주로 확장
    
    if not articles_df.empty:
        # CSV 파일로 저장
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"news_articles_{current_time}.csv"
        articles_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"\nCSV 파일이 저장되었습니다: {csv_filename}")
        
        # 뉴스 본문 추출
        texts, titles = crawler.extract_article_content(articles_df)
        
        # 결과 출력
        print(f"\n총 {len(texts)} 개의 유효한 뉴스 기사가 수집되었습니다.")
        
if __name__ == "__main__":
    main()