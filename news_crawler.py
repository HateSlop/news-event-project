from gdeltdoc import GdeltDoc, Filters
from newspaper import Article


def get_url(keyword, start_date, end_date, num_records=10, domain="nytimes.com", country="US"):
    """
    GDELT 데이터를 활용해 뉴스 URL 및 제목을 가져옵니다.
    """
    gd = GdeltDoc()
    
    # GDELT 검색 필터 설정
    filters = Filters(
        keyword=keyword,        # 검색 키워드
        start_date=start_date,  # 검색 시작 날짜
        end_date=end_date,      # 검색 종료 날짜
        num_records=num_records, # 가져올 기사 수
        domain=domain,          # 기사 도메인
        country=country         # 국가 코드
    )
    
    # 필터 조건에 맞는 기사를 검색
    articles = gd.article_search(filters)
    return articles


def get_article(df):
    """
    GDELT 데이터프레임에서 URL을 이용해 뉴스 텍스트를 크롤링합니다.
    """
    urls = df["url"]    # 데이터프레임에서 URL 열 추출
    titles = df["title"]  # 데이터프레임에서 제목 열 추출
    texts = []            # 기사 본문을 저장할 리스트 초기화
    
    for url in urls:
        try:
            article = Article(url)   # URL로부터 Article 객체 생성
            article.download()       # 기사 HTML 다운로드
            article.parse()          # 기사 본문 파싱
            texts.append(article.text)  # 파싱된 텍스트 저장
        except Exception as e:
            # 크롤링 실패 시 에러 출력 및 빈 텍스트 추가
            print(f"Error processing URL: {url}, Error: {e}")
            texts.append("")  # 실패한 경우 빈 텍스트 추가
    
    return texts, titles  # 크롤링된 기사 본문과 제목 리스트 반환
