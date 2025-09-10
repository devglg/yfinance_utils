#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
from yfinance_utils import constants, timing_utils, file_utils

FILENAME = 'weekly_price_rising'
filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

df = pd.DataFrame()
ticker_list = []
weeks_list = []
rise_pct = []
stars = []

for tick in filenames:
    try:
        data = file_utils.get_historic_data(tick)
        close = list(data['Close'])

        counter = 0
        star = ''
        for i in range(len(close)-1, 2, -1):
            counter = counter + 1
            if close[i] > close[i-1]:
                star = star + ' *'
                continue
            else:
                if counter > constants.MINIMUM_WEEKS_RISING:
                    ticker_list.append(tick)
                    weeks_list.append(counter)
                    rise_pct.append((close[-1] / close[counter]) * 100)
                    stars.append(star)
                break
    except Exception as e:
        continue

df['TICK'] = ticker_list
df['WEEKS'] = weeks_list
df['RISE PCT'] = rise_pct
df['WEEKS'] = stars

file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)

