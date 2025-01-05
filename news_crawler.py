from gdeltdoc import GdeltDoc, Filters
from newspaper import Article, Config
from datetime import datetime, timedelta
import pandas as pd
import time

#GDELT API를 사용하여 뉴스 URL을 수집
def get_news_urls(keywords, days):
    # gdeltdoc 객체 생성
    gd = GdeltDoc()
    all_articles = pd.DataFrame()

    for keyword in keywords:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 필터 설정: 날짜, 키워드, 뉴스 수 등
        filters = Filters(
            start_date=start_date.strftime("%Y-%m-%d"),  # 시작 날짜
            end_date=end_date.strftime("%Y-%m-%d"),      # 종료 날짜
            num_records=2,  # 뉴스 갯수
            keyword=keyword,  # 검색할 키워드
            country="US"  # 미국 뉴스로 한정
        )
        
        try:
            # GDELT API에서 뉴스 수집
            articles = gd.article_search(filters)
            if not articles.empty:
                # 날짜 컬럼 추가 (현재 수집 날짜 기준)
                articles['date'] = pd.to_datetime("today").strftime("%Y-%m-%d")
                all_articles = pd.concat([all_articles, articles])
                
            print(f"'{keyword}'의 {len(articles)}개 뉴스 수집 완료")
            time.sleep(1)  # 딜레이  

        except Exception as e:
            print(f"'{keyword}'의 뉴스 수집 중 오류 발생: {e}")
            continue

    # 중복된 url 제거
    all_articles = all_articles.drop_duplicates(subset=['url'])
    print(f"총 수집된 뉴스 갯수: {len(all_articles)}")
    return all_articles

#수집된 URL에서 뉴스 본문을 추출
def url_crawling(articles_df):
    texts = []
    titles = []
    
    # iterrows() - DataFrame의 각 행을 순서대로 순회하면서, (인덱스, 행 데이터) 형태로 반환
    for idx, row in articles_df.iterrows():
        try:

            config = Config()
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            #요청을 보낼 때 사용하는 브라우저의 user-agent 값을 설정
            config.browser_user_agent = user_agent
            # 서버와의 연결 시간, 응답 시간을 설정
            config.request_timeout = 10

            # 뉴스 기사의 URL로 기사 본문 찾기
            article = Article(row['url'], config=config)
            
            # URL에 있는 웹페이지의 HTML 소스 코드를 다운로드
            article.download()
            time.sleep(1)  
            # 기사에서 유용한 정보를 추출
            article.parse()
            
            # 빈 본문이나 짧은 본문은 제외
            if len(article.text.split()) > 50:
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
