# 해당 파일을 통해 크롤링, 분류, db 적재 기능이 실행되도록

from news_crawler import get_url, get_article
from news_classifier import chatgpt_generate
from prompt_template import prompt_template
from db_manager import write_data

companies = ["Microsoft", "Google", "Tesla"]

for company in companies:
    articles = get_url(company)
    texts, titles = get_article(articles)

    for i in range(10):
        answer = chatgpt_generate(prompt_template+texts[i])
        write_data(answer, company=company)