#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import math
from collections import Counter
from yfinance import Ticker as Ticker

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


def get_history(symbol):
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
    ANALYSTS - upgrades and downgrades
'''
def get_data(symbol):
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


def save_data(data, symbol, type):
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

"""
GET FINANCIAL STATEMENTS as dictionary
"""
def download_income_statement(symbol, periods = 1):
  ticker = Ticker(symbol)
  income = ticker.get_income_stmt()
  for i in range(periods):
    data = dict(income[ticker.get_income_stmt().columns[i]])
    save_data(data, symbol=symbol, type=f"IS{i}")
  return data

def download_balance_sheet(symbol, periods = 1):
  ticker = Ticker(symbol)
  balance = ticker.get_balance_sheet()
  for i in range(periods):
    data = dict(balance[ticker.get_balance_sheet().columns[i]])
    save_data(data, symbol=symbol, type=f"BS{i}")
  return data

def download_cashflow(symbol, periods = 1):
  ticker = Ticker(symbol)
  cash = ticker.get_cashflow()
  for i in range(periods):
    data = dict(cash[ticker.get_cashflow().columns[i]])
    save_data(data, symbol=symbol, type=f"CF{i}")
  return data


def get_income_statement(symbol, period = 0):
  data = get_data(symbol)
  return data[f'IS{period}']

def get_balance_sheet(symbol, period = 0):
  data = get_data(symbol)
  return data[f'BS{period}']

def get_cashflow(symbol, period = 0):
  data = get_data(symbol)
  return data[f'CF{period}']


"""
GET OTHER FINANCIAL INFORMATION

INFO
RATINGS
ANALYSTS RATINGS UPGRADE AND DOWNGRADES
NEWS
"""

def download_info(symbol):
  ticker = Ticker(symbol)
  d = ticker.info
  save_data(d, symbol=symbol, type='INFO')
  return d

def get_info(symbol):
  data = get_data(symbol)
  return data['INFO']

def download_ratings(symbol):
  ticker = Ticker(symbol)
  d = ticker.recommendations.iloc[0]
  up = d['strongBuy'] + d['buy']
  down = d['strongSell'] + d['sell']
  hold = d['hold']
  total = d['strongBuy'] + d['buy'] + d['strongSell'] + d['sell'] + d['hold']
  data = {'up':int(up), 'down': int(down), 'total': int(total), 'hold': int(hold)}
  save_data(data, symbol=symbol, type="RT")
  return data

def get_ratings(symbol):
  data = get_data(symbol)
  return data['RT']


def download_news(symbol):
  ticker = Ticker(symbol)
  d = ticker.news
  save_data(d, symbol=symbol, type='NEWS')
  return d

def get_news(symbol):
  news = get_data(symbol)
  return news['NEWS']


def download_analysts(symbol):
  t = Ticker(symbol)
  dupdown = t.get_upgrades_downgrades()
  grades = list(dupdown['ToGrade'])

  values = list(Counter(grades).values())
  keys = list(Counter(grades).keys())
  ratings = dict(zip(keys, values))
  save_data(ratings, symbol, type='ANALYSTS')
  return ratings

def get_analysts(symbol):
  an = get_data(symbol)
  return an['ANALYSTS']


def download_options(symbol):
    t = Ticker(symbol)
    options = t.option_chain()
    data = {}

    cv = list(options.calls['volume'])
    pv = list(options.puts['volume'])

    calls_volume = int(sum(x for x in cv if not math.isnan(x)))
    puts_volume = int(sum(x for x in pv if not math.isnan(x)))

    data['calls'] = calls_volume
    data['puts'] = puts_volume

    save_data(data, symbol=symbol, type='OPTIONS')
    return options

def get_options(symbol):
    op = get_data(symbol)
    return op['OPTIONS']


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
