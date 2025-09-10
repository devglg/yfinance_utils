#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
from yfinance_utils import file_utils, timing_utils, signals_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'HIGH', 'LOW', 'VOLUME', 'AVERAGE VOLUME']
FILENAME = 'daily_extremes_52_week_price'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.get_historic_data(tick)
        if signals_utils.is_price_year_high(data) or signals_utils.is_price_year_low(data):
            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  signals_utils.get_price_year_high(data),
                                  signals_utils.get_price_year_low(data),
                                  data['Volume'].iloc[-1]
                                  ]], columns=COLUMNS)

            df = pd.concat([df, tmp], ignore_index=True)
        else:
            pass

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
