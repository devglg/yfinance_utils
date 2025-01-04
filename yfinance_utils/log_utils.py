#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#


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
    try:
        log_to_mongo(file, msg)
    except Exception as e:
        print('Mongo not running. Saving logs to text file only.')
        
    file_utils.save_to_mongo
    create_folder()
    filename = f'{constants.OUTPUT_FOLDER}/{constants.LOG_FOLDER}/{constants.LOG_FILENAME}'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a') as f:
        f.write(f'{ts}, {file}, {msg}\n')
    f.close()

def log_to_mongo(file, msg):
    client = MongoClient('mongodb://localhost:27017/')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = client['market']
    collection = db['log']
    collection.insert_one({'timestamp':ts, 'script':file, 'log':msg})