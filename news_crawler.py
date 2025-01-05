from gdeltdoc import GdeltDoc, Filters
from newspaper import Article

gd = GdeltDoc()

# GDELT API를 이용하여 뉴스 기사 URL 가져오기
def get_url(keyword):
  f = Filters(
    start_date = "2024-05-01",
    end_date = "2024-05-25",
    num_records = 5,
    keyword = keyword,
    domain = "nytimes.com",
    country = "US",
  )
  articles = gd.article_search(f)

  if articles.empty:
    raise ValueError(f"No articles found for keyword: {keyword}")
  
  return articles

# 뉴스 기사 URL을 이용하여 뉴스 기사 내용 가져오기
def get_article(df):
  
  if df.empty:
    raise ValueError("The DataFrame is empty.")
  
  urls = df["url"]
  titles = df["title"]
  texts = []
  for url in urls:
    article = Article(url)
    article.download()
    article.parse()
    texts.append(article.text)
  return texts, titles
