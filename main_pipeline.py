from news_crawler import get_url, get_article
from news_classifier import chatgpt_generate
from prompt_template import prompt_template
from db_manager import write_data

companies = ["Apple", "Nvidia", "Microsoft"]

for company in companies:
    articles = get_url(company)
    texts, titles = get_article(articles)

    for i in range(10):
        answer = chatgpt_generate(prompt_template+texts[i])
        write_data(answer, company=company)