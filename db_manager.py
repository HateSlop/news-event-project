import json
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

#뉴스 기사 데이터를 MongoDB에 저장합니다.
def save_news_results(raw_data, company):
    mongo_client = MongoClient(host="localhost", port=27017)
    db = mongo_client["news"]  # MongoDB 클라이언트
    collection = db[company]  # 회사 이름으로 컬렉션 가져오기
    data = json.loads(raw_data)
    collection.insert_one(data)

def fetch_data(company):
    mongo_client = MongoClient(host="localhost", port=27017)
    db = mongo_client["news"]  # MongoDB 클라이언트
    collection = db[company]  # 회사 이름으로 컬렉션 가져오기
    data = list(collection.find({}, {"_id": 0}))  # _id 필드를 제외한 데이터를 가져옴
    return pd.DataFrame(data)

def delete_data(company):
    mongo_client = MongoClient(host="localhost", port=27017)
    db = mongo_client["news"] #client 생성
    collection = db[company]
    result = collection.delete_many({})
    print(f"{result.deleted_count} documents have been deleted.")
