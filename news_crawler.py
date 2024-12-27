# 크롤링 관련 기능
# 1. 뉴스 데이터 수집
# 2. 뉴스 크롤링 및 텍스트 추출

# GDELT 데이터를 활용해 뉴스 기사를 수집

from gdeltdoc import GdeltDoc, Filters
from newspaper import Article


def get_url(keyword):
    gd = GdeltDoc()
    f=Filters(
        keyword = keyword,
        start_date = "2024-05-01",
        end_date = "2024-07-28",
        num_records=10,
        domain ="nytimes.com",
        country="US",
    )
    articles = gd.article_search(f)
    return articles

def get_article(df):
    urls = df["url"]
    titles = df["title"]
    texts = []
    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        texts.append(article.text)
    return texts, titles
