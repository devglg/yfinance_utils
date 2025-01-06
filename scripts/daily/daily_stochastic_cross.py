#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import math
import pandas as pd
from yfinance_utils import file_utils, timing_utils, signals_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'VOL']
FILENAME = 'daily_stochastic_cross'

df = pd.DataFrame(columns=COLUMNS)
filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if math.isnan(data['Close'].iloc[-1]): continue

        if (
            signals_utils.is_ma_bullish_trend(data) and \
            signals_utils.is_stochastic_cross_down(data, days_back=3, line=20)
            ) or (
            signals_utils.is_ma_bearish_trend(data) and \
            signals_utils.is_stochastic_cross_up(data, days_back=3, line=80)
            ):

            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1]
                                  ]], columns=COLUMNS)
            df = pd.concat([df, tmp], ignore_index=True)
        else:
            pass

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
