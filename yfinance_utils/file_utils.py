#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import os
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from datetime import date
from yfinance_utils import constants
from pprint import pprint

def save_output_file(df, name):
    try:
        if os.environ['YFU_PRINT_OUT']:
            pprint(df)
    except Exception as e:
        pass

    try:
        save_to_mongo(df, name)
    except Exception as e:
        print('Mongo not running. Saving to output directory only. This will soon change to only save to the database.')
    
    folder_path = f'{constants.OUTPUT_FOLDER}/{name}'
    try:
        os.mkdir(folder_path)
    except Exception as e:
        pass

    filepath = f'{constants.OUTPUT_FOLDER}/{name}/{str(date.today())}_{name}.csv'
    if 'TICK'in df.columns:
        ticks = df['TICK']
        url = []
        for i in ticks:
            url.append(f'{constants.QUOTE_BASE_URL}/{i}/')
        df['URL'] = url
    df.round(2).to_csv(filepath, index=False)

def read_historic_data(name):
    name = f'{constants.DATA_FOLDER}/{name}'
    return pd.read_csv(name, index_col=0)

def save_historic_data(df, name):
    name = f'{constants.DATA_FOLDER}/{name}'
    try:
        os.mkdir(constants.DATA_FOLDER)
    except Exception as e:
        pass
    return df.to_csv(name)

def get_scripts_folder(t='daily'):
    if 'W' in t.upper():
        return constants.SCRIPTS_FOLDER_WEEKLY
    else:
        return constants.SCRIPTS_FOLDER_DAILY
    
def get_datasets_list():
    return os.listdir(constants.DATA_FOLDER)

def save_to_mongo(data, name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bigdata']
    collection = db['market']
    recs = []

    if isinstance(data, dict):
        recs.extend(data)
    else:
        recs.extend(data.to_dict('records'))
    
    def update_dicts_in_list(list_of_dicts, key, value):
        for d in list_of_dicts:
            d[key] = value

    if recs:
        update_dicts_in_list(recs, "timestamp", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        update_dicts_in_list(recs, "script", name)
        collection.insert_many(recs)
