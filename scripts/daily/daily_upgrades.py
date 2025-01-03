#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

# TODO: change to recommentations_summary
'''
>>> t.recommendations
  period  strongBuy  buy  hold  sell  strongSell
0     0m          8   24    12     1           2
1    -1m          8   24    12     1           2
2    -2m          8   24    12     1           2
3    -3m          8   23    12     1           2
>>> 
'''


import pandas as pd
from yfinance import Tickers
from yfinance_utils import financials_utils, file_utils, timing_utils, constants

COLUMNS = ['DATE', 'TICK', 'GOOD', 'BAD', 'NEUTRAL', 'TOTAL', 'AVG', 'UP_DOWN']
FILENAME_UP = 'daily_analysts_up'
FILENAME_DOWN = 'daily_analysts_down'

dfups = pd.DataFrame(columns=COLUMNS)
dfdowns = pd.DataFrame(columns=COLUMNS)

t_list = file_utils.get_datasets_list()
start_time = timing_utils.start(t_list, f'{FILENAME_UP}-{FILENAME_DOWN}')

ts = Tickers(t_list)

for tick in ts.tickers:
    try:
        t = ts.tickers[tick]
        data = file_utils.read_historic_data(tick)
        tmp = financials_utils.get_ratings(t)

        up = tmp['up']
        down = tmp['down'] 
        good = tmp['up'] + tmp['Buy'] + tmp['Outperform'] + tmp['Overweight'] 
        bad = tmp['down'] + tmp['Underweight'] + tmp['Underperform'] 
        neutral = tmp['Hold'] + tmp['Neutral'] + tmp['Equal-Weight'] + tmp['Sector Weight']

        total = good + bad + neutral
        avg = good / total * 100

    except Exception as e:
        continue
    
    if avg > constants.PERCENTAGE_GOOD_RATING:
        if up > down:
            tmp =  pd.DataFrame([[data.index[-1], tick, good, bad, neutral, total, avg, up - down]], columns=COLUMNS)
            dfups = pd.concat([dfups, tmp], ignore_index=True)
        else:
            tmp =  pd.DataFrame([[data.index[-1], tick, good, bad, neutral, total, avg, up - down]], columns=COLUMNS)
            dfdowns = pd.concat([dfdowns, tmp], ignore_index=True)

file_utils.save_output_file(dfups,FILENAME_UP)
file_utils.save_output_file(dfdowns,FILENAME_DOWN)
timing_utils.end(start_time, f'{FILENAME_UP}-{FILENAME_DOWN}')
