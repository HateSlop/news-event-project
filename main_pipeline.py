import config
from prompt_template import prompt_template
from news_crawler import get_url, get_article
from news_classifier import chatgpt_generate
from db_manager import insert_into_db
import json
import datetime

def analysis():
    orgs = ["microsoft", "apple", "google"]  # 분석할 기업 이름을 저장한 리스트

    for org in orgs:  
        df = get_url(org)  # `get_url` 함수를 호출하여 해당 기업과 관련된 데이터를 가져옴
        dates = df["seendate"]  # 데이터프레임에서 기사 날짜 정보를 가져옴
        texts, titles = get_article(df)  # `get_article` 함수로 기사 본문과 제목을 가져옴
        
        for idx, text in enumerate(texts):  # 가져온 기사 본문에 대해 반복
            news_item = {}  # 개별 뉴스 아이템을 저장할 딕셔너리
            answer = chatgpt_generate(prompt_template + text)  # GPT 모델로 기사 분석
            
            try:
                # GPT 응답을 JSON으로 안전하게 변환
                answer_dict = json.loads(answer)
                
                # Task #1: 카테고리
                category = answer_dict.get("문서 카테고리", [])
                
                # Task #2: 요약
                summary = answer_dict.get("요약", "")
                
                # Task #3: 주요 이벤트
                events = answer_dict.get("주요 이벤트", [])
                
                # news_item에 데이터 추가
                news_item["com"] = org  # 기업 이름(org) 추가
                news_item["text"] = text  # 기사 본문 저장
                news_item["title"] = titles[idx]  # 기사 제목 저장
                news_item["category"] = category  # 카테고리 저장
                news_item["summary"] = summary  # 요약 저장
                news_item["events"] = events  # 주요 이벤트 저장
                news_item["seendate"] = dates[idx]  # 기사 날짜 저장
                news_item["date"] = datetime.datetime.now()  # 현재 날짜와 시간 저장
                
                print("Inserting data:", news_item)  # 삽입 직전 데이터 출력
                insert_into_db(news_item)  # DB에 저장

            except Exception as e:
                print(f"Error processing article: {e}")
                continue  # 에러 발생 시 해당 루프를 건너뜀

    return  # 함수 종료

analysis()
