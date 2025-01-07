#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import math
from yfinance_utils import file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'HIGH', 'CLOSE', 'OPEN', 'CLOSE -1']
FILENAME = 'daily_gap_up_close_high'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        vol_avg = data['Volume'].rolling(window=10).mean().iloc[-1]

        def gap_up():
            return data['Open'].iloc[-1] > data['Close'].iloc[-2]
        
        def close_high():
            return data['Close'].iloc[-1] > data['Open'].iloc[-1] \
                   and math.isclose(data['Close'].iloc[-1],data['High'].iloc[-1],abs_tol=(data['High'].iloc[-1]*.005))

        if gap_up() and close_high():
            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['High'].iloc[-1],
                                  data['Close'].iloc[-1],
                                  data['Open'].iloc[-1],
                                  data['Close'].iloc[-2],
                                  ]], columns=COLUMNS)
    
            df = pd.concat([df, tmp], ignore_index=True)

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
