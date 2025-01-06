#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import statistics
from finta import TA
from yfinance_utils import rsi_utils, file_utils, constants, timing_utils

COLUMNS = ['DATE', 'TICK', 'RSI', 'AVERAGE', 'PRICE -1', 'VOLUME -1', 'VOL % -1', 'PRICE', 'VOLUME', 'VOL %']
FILENAME = 'daily_jump_volume'

dfvol = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        d_rsi = TA.RSI(data.iloc[-constants.TRADING_DAYS_IN_YEAR:], period=14)
        if d_rsi['rsi'].iloc[-1] < constants.MINIMUM_RSI:
            continue

        avg = d_rsi['Volume'].rolling(10).mean().iloc[-1]
        volume_0 = d_rsi['Volume'].iloc[-1]
        volume_0_pct = volume_0/avg*100
        volume_1 = d_rsi['Volume'].iloc[-2]
        volume_1_pct = volume_1/avg*100

        price_0 = d_rsi['Close'].iloc[-1]
        price_1 = d_rsi['Close'].iloc[-2]

        rsi = d_rsi['rsi'].iloc[-1]
    except Exception as e:
        continue
    
    if volume_0_pct > 150 and volume_1_pct < 110:
        tmpvol =  pd.DataFrame([[data.index[-1], tick, rsi, avg, price_1, volume_1, volume_1_pct, price_0, volume_0, volume_0_pct]], columns=COLUMNS)
        dfvol = pd.concat([dfvol, tmpvol], ignore_index=True)

file_utils.save_output_file(dfvol,FILENAME)
timing_utils.end(start_time, FILENAME)
