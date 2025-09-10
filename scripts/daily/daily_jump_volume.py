#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
from yfinance_utils import file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'AVERAGE', 'PRICE', 'VOLUME', 'VOL %']
FILENAME = 'daily_jump_volume'

dfvol = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.get_historic_data(tick)
        avg = data['Volume'].rolling(10).mean().iloc[-1]
        volume_0 = data['Volume'].iloc[-1]
        volume_0_pct = volume_0/avg*100
        price_0 = data['Close'].iloc[-1]
    except Exception as e:
        continue
    
    if volume_0_pct > 150:
        tmpvol =  pd.DataFrame([[data.index[-1][:10], tick, avg, price_0, volume_0, volume_0_pct]], columns=COLUMNS)
        dfvol = pd.concat([dfvol, tmpvol], ignore_index=True)

file_utils.save_output_file(dfvol,FILENAME)
timing_utils.end(start_time, FILENAME)
