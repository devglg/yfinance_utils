#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import datetime
import pandas as pd
from yfinance import Tickers
from yfinance_utils import file_utils, file_utils, timing_utils, list_utils

COLUMNS = ['DATE', 'TICK', 'UP', 'DOWN', 'HOLD', 'AVG', 'TOTAL']
FILENAME='daily_analysts_ratings'

dfups = pd.DataFrame(columns=COLUMNS)
filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

# ETFs do not get ratings from analysts
remove_etfs = ['SPY', 'VTI', 'MID', 'QQQ', 'VOO', 'USD', 'VGT', 'DIA', 'FOX'] + list_utils.get_sectors()
filenames = list(set(filenames) - set(remove_etfs))

for symbol in filenames:
    try:
        # TODO: change this to t.recommendstions
        tmp = file_utils.get_ratings(symbol)
        up = tmp['up']
        down = tmp['down']
        hold = tmp['hold']
        total = tmp['total']
        avg_up = up / total * 100

    except Exception as e:
        continue
    
    if avg_up > 85:
        tmpups =  pd.DataFrame([[datetime.date.today().strftime('%Y-%m-%d'), symbol, up, down, hold, avg_up, total]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)

file_utils.save_output_file(dfups,FILENAME)
timing_utils.end(start_time, FILENAME)