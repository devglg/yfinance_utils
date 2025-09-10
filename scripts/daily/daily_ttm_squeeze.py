#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from finta import TA
from yfinance_utils import file_utils, constants, timing_utils

FILENAME = 'daily_ttm_squeeze'
COLUMNS=['DATE', 'TICK', 'DAYS']

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.get_history(tick)
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE: continue

        data = pd.concat([data, TA.BBANDS(data)], axis=1)
        data = pd.concat([data, TA.KC(data, kc_mult=1.5, atr_period=20)], axis=1)
        data['BB_SQUEEZE_IN'] = data['BB_UPPER'] < data['KC_UPPER']
        
        last = []
        for i in range(-1,-5,-1):
            last.append(data['BB_SQUEEZE_IN'].iloc[i])

        def days_in_squeeze(data):
            for i in range(-2, -50, -1):
                if data['BB_SQUEEZE_IN'].iloc[i]:
                    continue
                else:
                    return abs(i) - 1 
            
        days = 0
        if not data['BB_SQUEEZE_IN'].iloc[-1] and data['BB_SQUEEZE_IN'].iloc[-2]:
            days = days_in_squeeze(data)
        else:
            continue  

        if days < constants.MINIMUM_DAYS_SQUEEZE: continue

        if data['Close'].iloc[-1] > data['BB_MIDDLE'].iloc[-1]:
            tmp = pd.DataFrame([[data.index[-1], tick, days ]], columns=COLUMNS)  
            df = pd.concat([df,tmp], ignore_index=True)

    except Exception as e:
        pass

file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
