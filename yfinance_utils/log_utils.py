import os
from pymongo import MongoClient
from datetime import datetime
from yfinance_utils import constants, file_utils

def create_folder():
    try:
        os.mkdir(f'{constants.OUTPUT_FOLDER}/{constants.LOG_FOLDER}')
    except Exception as e:
        pass

def log(file, msg):
    log_to_mongo(file, msg)
    file_utils.save_to_mongo
    create_folder()
    filename = f'{constants.OUTPUT_FOLDER}/{constants.LOG_FOLDER}/{constants.LOG_FILENAME}'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a') as f:
        f.write(f'{ts}, {file}, {msg}\n')
    f.close()

def log_to_mongo(file, msg):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['log']
    collection = db[file]
    collection.insert_one(msg)