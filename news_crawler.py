from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
import pandas as pd


def get_url(keyword):
    if not keyword or len(keyword) < 3:
        raise ValueError("Keyword must be at least 3 characters long.")
    
    gd = GdeltDoc()
    f=Filters(
        keyword = keyword,
        start_date = "2024-07-01",
        end_date = "2024-11-30",
        num_records=10,
        domain ="nytimes.com",
        country="US",
    )
    try:
        articles = gd.article_search(f)
        return articles
    except ValueError as e:
        print(f"Error during API call: {e}")
        return []


def get_article(articles):
    if not articles:
        print("No articles found.")
        return [], [], []    

    df = pd.DataFrame(articles)
    
    if df.empty or "url" not in df.columns or "title" not in df.columns:
        print("No valid articles in DataFrame.")
        return [], [], []
    
    urls = df["url"]
    titles = df["title"]
    texts = []
    dates = []

    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            texts.append(article.text)
            dates.append(article.publish_date)
        except Exception as e:
            texts.append(None)
            dates.append(None)
            print(f"Failed to process article at {url}: {e}")

    return texts, titles, dates