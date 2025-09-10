#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import os, json
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
        if os.environ['MONGO']:
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
            if os.path.exists(f'{constants.OUTPUT_FOLDER}/FIDELITY'):
                url.append(f'{constants.FIDELITY_BASE_URL}{i}')
            else:
               url.append(f'{constants.QUOTE_BASE_URL}/{i}/')
    
        df['URL'] = url
    df.round(2).to_csv(filepath, index=False)





def get_historic_data(symbol):
    current_dir = os.getcwd()
    current_file = os.path.basename(current_dir)

    while not current_file == 'yfinance_utils':
        os.chdir('../')
        current_dir = os.getcwd()
        current_file = os.path.basename(current_dir)
        
    path = f'{constants.DATA_FOLDER}/{symbol}'
    try:
        data = pd.read_csv(path, index_col=0)
    except Exception:
        return None
    return data

def save_historic_data(df, symbol):
    current_dir = os.getcwd()
    current_file = os.path.basename(current_dir)

    while not current_file == 'yfinance_utils':
        os.chdir('../')
        current_dir = os.getcwd()
        current_file = os.path.basename(current_dir)

    path = f'{constants.DATA_FOLDER}/{symbol}'
    try:
        os.mkdir(constants.DATA_FOLDER)
    except Exception as e:
        pass
    return df.to_csv(path)


###############################################################
###############################################################
'''
type: 
    IS - income statement
    BS - Balance Sheet
    CF - Cash Flow
    RT - Ratings
    NEWS - News
'''
def get_financials(symbol):
    current_dir = os.getcwd()
    current_file = os.path.basename(current_dir)
    read_data = {}
    while not current_file == 'yfinance_utils':
        os.chdir('../')
        current_dir = os.getcwd()
        current_file = os.path.basename(current_dir)
        
    path = f'{constants.FINANCIALS_FOLDER}/{symbol}'
    try:
        with open(path, "r") as file:
            read_data = json.load(file)
            return read_data
    except Exception:
        print(f'error reading {path}')
        return None


def save_financials(data, symbol, type):
    current_dir = os.getcwd()
    current_file = os.path.basename(current_dir)

    while not current_file == 'yfinance_utils':
        os.chdir('../')
        current_dir = os.getcwd()
        current_file = os.path.basename(current_dir)

    path = f'{constants.FINANCIALS_FOLDER}/{symbol}'
    try:
        os.mkdir(constants.FINANCIALS_FOLDER)
    except Exception as e:
        pass

    if not os.path.exists(path):
        content={}
        content[type] = data
        with open(path, "w") as file:
            json.dump(content, file, indent=4)   
    else:
        content = {}
        with open(path, "r") as file:
            content = json.load(file)
        content[type] = data
        with open(path, "w") as file:
            json.dump(content, file, indent=4)       
    
    return data

###############################################################
###############################################################



### utilities


def get_scripts_folder(t='daily'):
    if 'W' in t.upper():
        return constants.SCRIPTS_FOLDER_WEEKLY
    else:
        return constants.SCRIPTS_FOLDER_DAILY
    


def get_python_executable():
    return constants.PYTHON_EXE
    


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
