#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
from yfinance_utils import file_utils, timing_utils

FILENAME = 'daily_volume_total'
dfvol = pd.DataFrame()

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if not 'DATE' in dfvol.columns:
            dfvol['DATE'] = data.index
            dfvol.set_index('DATE', inplace=True)

        dfvol[tick] = data['Volume']

    except Exception as e:
        continue

dfvol['TOTAL'] = dfvol.sum(axis=1)
dfvol.reset_index(inplace=True)

file_utils.save_output_file(dfvol, FILENAME)
timing_utils.end(start_time, FILENAME)
