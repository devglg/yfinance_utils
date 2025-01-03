#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

RATINGS = ['Buy', 'Hold', 'Neutral', 'Outperform', 'Overweight', 'Underweight', 'Equal-Weight', 'Underperform', 'Market Perform', 'Sector Weight', 'Sector Perform', 'Gradually Accumulate']


"""
GET FINANCIAL STATEMENTS as dictionary
"""
def get_is(ticker, period = 0):
  return dict(ticker.get_income_stmt()[ticker.get_income_stmt().columns[period]])

def get_bs(ticker, period = 0):
  return dict(ticker.get_balance_sheet()[ticker.get_balance_sheet().columns[period]])

def get_cashflow(ticker, period = 0):
  return dict(ticker.get_cashflow()[ticker.get_cashflow().columns[period]])



"""
GET OTHER FINANCIAL INFORMATION
"""

def get_ratings(ticker):
  d = ticker.recommendations.iloc[0]
  up = d['strongBuy'] + d['buy']
  down = d['strongSell'] + d['sell']
  hold = d['hold']
  total = d['strongBuy'] + d['buy'] + d['strongSell'] + d['sell'] + d['hold']
  stats = {'up':up, 'down': down, 'total': total, 'hold':hold}
  return stats

def get_historic_price(ticker, price_field = 'Close'):
  d = ticker.history()
  return list(d[price_field])

def get_last_price(tick):
  d = get_historic_price(tick)
  if len(d) < 1:
    return None
  return d[-1]




