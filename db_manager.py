from pymongo import MongoClient
import pandas as pd
import json

def get_mongo_collection(company, db_name="project_07", uri="mongodb://localhost:27017/"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[company]

def write_data(raw_data, company):
    collection = get_mongo_collection(company)
    data = json.loads(raw_data)
    collection.insert_one(data)

def fetch_data(company):
    collection = get_mongo_collection(company)
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

def delete_data(company):
    collection = get_mongo_collection(company)
    result = collection.delete_many({})
    print(f"{result.deleted_count} documents have been deleted from collection: {company}")
