#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import math
import pandas as pd
from yfinance_utils import rsi_utils, file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'RSI', 'RSI_MINIMUM', 'RSI_MAXIMUM', 'RSI_AVERAGE', 'VOLUME']

FILENAME = 'daily_rsi_year_extremes'

dfrsi = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, f'{FILENAME}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        df_rsi = rsi_utils.get_rsi(data)

        rsi = df_rsi['rsi'].iloc[-1]
        rsimin = df_rsi['rsi'].min()
        rsimax = df_rsi['rsi'].max()
        rsiavg = df_rsi['rsi'].mean()
        price = df_rsi['Close'].iloc[-1]
        vol = df_rsi['Volume'].iloc[-1]

    except Exception as e:
        continue
    
    tmprsi =  pd.DataFrame([[data.index[-1], tick, price, rsi, rsimin, rsimax, rsiavg, vol]], columns=COLUMNS)
    if math.isclose(rsi,rsimin, abs_tol=2) or math.isclose(rsi,rsimax, abs_tol=2) :
        dfrsi = pd.concat([dfrsi, tmprsi], ignore_index=True)
    else:
        continue
        
file_utils.save_output_file(dfrsi,FILENAME)
timing_utils.end(start_time, f'{FILENAME}')
