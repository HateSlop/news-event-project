import json
import datetime
from pymongo import MongoClient
import pandas as pd

mongo_client = MongoClient(host="localhost", port=27017)
db = mongo_client["news-event-project"]

def write_data(raw_data, company):
    collection = db[company]
    data = json.loads(raw_data)
    collection.insert_one(data)

def fetch_data(company):
    collection = db[company]
    data_list = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data_list)
    return df
