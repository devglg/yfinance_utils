#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import math
import pandas as pd
from yfinance_utils import mfi_utils, file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'MFI', 'MFI_AVERAGE', 'VOLUME']

FILENAME_MIN = 'daily_mfi_year_lowest'
FILENAME_MAX = 'daily_mfi_year_highest'

dfmfimin = pd.DataFrame(columns=COLUMNS)
dfmfimax = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()

start_time = timing_utils.start(filenames, f'{FILENAME_MIN}-{FILENAME_MAX}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        df_mfi = mfi_utils.get_mfi(data)

        mfi = df_mfi['mfi'].iloc[-1]
        mfimin = df_mfi['mfi'].min()
        mfimax = df_mfi['mfi'].max()
        mfiavg = df_mfi['mfi'].mean()
        price = df_mfi['Close'].iloc[-1]
        vol = df_mfi['Volume'].iloc[-1]

    except Exception as e:
        continue
    
    tmpmfi =  pd.DataFrame([[data.index[-1], tick, price, mfi, mfiavg, vol]], columns=COLUMNS)

    if math.isclose(mfi,mfimin, abs_tol=2):
        dfmfimin = pd.concat([dfmfimin, tmpmfi], ignore_index=True)

    elif math.isclose(mfi,mfimax, abs_tol=2):
        dfmfimax = pd.concat([dfmfimax, tmpmfi], ignore_index=True)

    else:
        continue
        
file_utils.save_output_file(dfmfimin, FILENAME_MIN)
file_utils.save_output_file(dfmfimax, FILENAME_MAX)
timing_utils.end(start_time, f'{FILENAME_MIN}-{FILENAME_MAX}')
