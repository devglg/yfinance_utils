#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from finta import TA
from yfinance_utils import file_utils, constants, timing_utils, signals_utils, utils

FILENAME_UP = 'daily_cross'
COLUMNS=['DATE', 'TICK', 'CROSS']

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME_UP)

for tick in filenames:
    try:
        data = file_utils.get_historic_data(tick)
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE: continue

        if signals_utils.is_ma_cross_up(data):
            df = utils.add_row_to_df(df, [data.index[-1], tick, 'UP' ],COLUMNS)  

        elif signals_utils.is_ma_cross_down(data):
            df = utils.add_row_to_df(df, [data.index[-1], tick, 'DOWN'],COLUMNS)  

    except Exception as e:
        pass

file_utils.save_output_file(df,FILENAME_UP)
timing_utils.end(start_time, FILENAME_UP)
