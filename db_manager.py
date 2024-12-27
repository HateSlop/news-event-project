# db 적재 기능
# 4. 데이터베이스 저장

# 뉴스에서 추출하고 요약한 결과를 MongoDB에 저장
from pymongo import MongoClient
import pandas as pd
import json

def write_data(raw_data, company):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['project_07']
    collection = db[company]
    data = json.loads(raw_data)
    collection.insert_one(data)

def fetch_data(company):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['project_07']
    collection = db[company]
    data = list(collection.find())
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

def delete_data(company):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['project_07']
    collection = db[company]
    result = collection.delete_many({})
    print(f"{result.deleted_count} documents have been deleted.")

