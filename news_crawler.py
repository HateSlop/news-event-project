from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
import pandas as pd

def get_url(keyword):
    f = Filters(
        start_date="2024-01-01",
        end_date="2024-05-10",
        num_records=10,
        keyword=keyword,
        domain="nytimes.com",
        country="US",
    )

    gd = GdeltDoc()  # GdeltDoc 클래스의 인스턴스 생성
    articles = gd.article_search(f)  # Gdelt 데이터베이스에서 필터를 적용한 기사 검색
    return articles

def get_article(df):
    urls = df["url"]
    titles = df["title"]

    texts = []
    dates = []

    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        texts.append(article.text)
        dates.append(article.publish_date)

    return texts, titles, dates
