import json
import datetime

from news_crawler import get_url, get_article
from news_classifier import chatgpt_generate
from prompt_template import prompt_template
from db_manager import write_data

companies = ["Nvidia", "Apple", "Tesla"]

for company in companies:
    print(f"[INFO] Processing company: {company}")

    # 1) GDELT에서 기사 목록 가져오기
    articles = get_url(company)
    print(f"[INFO] Number of articles fetched: {len(articles)}")
    # 2) Newspaper3k로 각 기사 본문/발행일 추출
    texts, titles, pub_dates = get_article(articles)
    print(f"[INFO] Successfully extracted texts from articles.")

    for i in range(min(10, len(texts))):
        print(f"[INFO] Processing article {i+1} for {company}...")
        pub_date = pub_dates[i]
        prompt = prompt_template + texts[i]
        answer = chatgpt_generate(prompt)

        # 4) JSON 파싱
        parsed_answer = json.loads(answer)
        doc_category = parsed_answer["문서 카테고리"]  
        main_event   = parsed_answer["주요 이벤트"]        

        # 5) DB에 넣을 데이터 구성
        data_dict = {
            "date": pub_date,
            "title": titles[i],
            "text": texts[i],
            "문서 카테고리": doc_category,
            "주요 이벤트": main_event,
            "요약": answer
        }

        # 6) JSON으로 직렬화 후 DB에 write
        raw_data = json.dumps(data_dict, default=str)
        write_data(raw_data, company=company)

    print(f"[INFO] Finished processing {company}.\n")
