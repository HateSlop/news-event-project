import config
from prompt_template import prompt_template
from pymongo import MongoClient
import pandas as pd

mongo_client = MongoClient(host="localhost", port=27017)
db = mongo_client["NewsProject"]
collection = db["NewsAnalysisDate"]

# MongoDB에 데이터를 저장하는 함수
def insert_into_db(news_item):
    try:
        insert_id = collection.insert_one(news_item).inserted_id
        print(f"Data inserted with ID: {insert_id}")
    except Exception as e:
        print(f"Error inserting data into DB: {e}")

def fetch_data(company):
    try:
        collection = db["NewsAnalysisDate"]  # 모든 데이터는 "NewsAnalysisDate" 컬렉션에 있다고 가정
        
        # "org" 값이 company와 일치하는 데이터만 조회
        data_list = list(collection.find({"com": company}, {"_id": 0}))
        
        if not data_list:
            print(f"No data found for company: {company}")
            return pd.DataFrame()  # 빈 DataFrame 반환
        
        df = pd.DataFrame(data_list)
        print(f"Fetched {len(df)} records for company: {company}")
        return df
    except Exception as e:
        print(f"Error fetching data for company {company}: {e}")
        return pd.DataFrame()  # 오류 발생 시 빈 DataFrame 반환

