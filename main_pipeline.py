import json
import datetime

from news_crawler import get_url, get_article
from news_classifier import chatgpt_generate
from prompt_template import prompt_template
from db_manager import write_data

companies = ['Nvidia', 'Google', "Microsoft"]

for company in companies:

    try:
        articles = get_url(company)
        texts, titles, dates = get_article(articles)

        if not texts or not titles or not dates:
            print(f"No valid articles found for {company}.")
            continue

        for i in range(10):
            if texts[i] is None or dates[i] is None:
                continue
    
            date = dates[i]
            prompt = prompt_template + texts[i]
            answer = chatgpt_generate(prompt)

            parsed_answer = json.loads(answer)
            doc_category = parsed_answer.get("Category", "Unknown")
            main_event = parsed_answer.get("Main Event", "Unknown")

            data_dict = {
                "date": date,
                "title": titles[i],
                "text": texts[i],
                "Category": doc_category,
                "Main Event": main_event,
                "Summary": answer,
            }

            raw_data = json.dumps(data_dict, default=str)
            write_data(raw_data, company=company)
    
    except ValueError as e:
        print(f"Error processing company {company}: {e}")