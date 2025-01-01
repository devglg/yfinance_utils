#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import math
from yfinance_utils import file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'PRICE 1', 'PRICE 2', 'PRICE 3']
FILENAME = 'daily_GAP_UP_CLOSE_HIGH'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, f'{FILENAME}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        vol_avg = data['Volume'].rolling(window=10).mean().iloc[-1]

        def gap_up():
            return data['Open'].iloc[-2] > data['Close'].iloc[-3] and \
                   data['Open'].iloc[-1] > data['Close'].iloc[-2]
        
        def close_high():
            return math.isclose(data['Close'].iloc[-2],data['High'].iloc[-2],abs_tol=(data['High'].iloc[-2]*.05)) and \
                   math.isclose(data['Close'].iloc[-3],data['High'].iloc[-3],abs_tol=(data['High'].iloc[-2]*.05))

        def vol_up():
            return data['Volume'].iloc[-2] > vol_avg and \
                   data['Volume'].iloc[-3] > vol_avg

        if gap_up() and close_high() and vol_up():
            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Close'].iloc[-2],
                                  data['Close'].iloc[-3],
                                  ]], columns=COLUMNS)
    
            df = pd.concat([df, tmp], ignore_index=True)

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, f'{FILENAME}')
