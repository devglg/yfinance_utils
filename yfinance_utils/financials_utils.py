#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

from collections import Counter
from yfinance import Ticker as Ticker
from yfinance_utils import file_utils

"""
GET FINANCIAL STATEMENTS as dictionary
"""
def download_income_statement(symbol, period = 0):
  ticker = Ticker(symbol)
  data = dict(ticker.get_income_stmt()[ticker.get_income_stmt().columns[period]])
  file_utils.save_financials(data, symbol=symbol, type="IS")
  return data

def download_balance_sheet(symbol, period = 0):
  ticker = Ticker(symbol)
  data = dict(ticker.get_balance_sheet()[ticker.get_balance_sheet().columns[period]])
  file_utils.save_financials(data, symbol=symbol, type="BS")
  return data

def download_cashflow(symbol, period = 0):
  ticker = Ticker(symbol)
  data = dict(ticker.get_cashflow()[ticker.get_cashflow().columns[period]])
  file_utils.save_financials(data, symbol=symbol, type="CF")
  return data



def get_income_statement(symbol):
  data = file_utils.get_financials(symbol)
  return data['IS']

def get_balance_sheet(symbol):
  data = file_utils.get_financials(symbol)
  return data['BS']

def get_cashflow(symbol):
  data = file_utils.get_financials(symbol)
  return data['CF']



"""
GET OTHER FINANCIAL INFORMATION
"""

def download_ratings(symbol):
  ticker = Ticker(symbol)
  d = ticker.recommendations.iloc[0]
  up = d['strongBuy'] + d['buy']
  down = d['strongSell'] + d['sell']
  hold = d['hold']
  total = d['strongBuy'] + d['buy'] + d['strongSell'] + d['sell'] + d['hold']
  data = {'up':int(up), 'down': int(down), 'total': int(total), 'hold': int(hold)}
  file_utils.save_financials(data, symbol=symbol, type="RT")
  return data

def get_ratings(symbol):
  data = file_utils.get_financials(symbol)
  return data['RT']


def download_news(symbol):
  ticker = Ticker(symbol)
  d = ticker.news
  file_utils.save_financials(d, symbol=symbol, type='NEWS')
  return d

def get_news(symbol):
  news = file_utils.get_financials(symbol)
  return news['NEWS']


def download_analysts(symbol):
  t = Ticker(symbol)
  dupdown = t.get_upgrades_downgrades()
  grades = list(dupdown['ToGrade'])

  values = list(Counter(grades).values())
  keys = list(Counter(grades).keys())
  ratings = dict(zip(keys, values))
  file_utils.save_financials(ratings, symbol, type='ANALYSTS')
  return ratings

def get_analysts(symbol):
  an = file_utils.get_financials(symbol)
  return an['ANALYSTS']
