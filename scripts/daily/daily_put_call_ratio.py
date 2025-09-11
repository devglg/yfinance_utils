#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import math
import yfinance
from yfinance_utils import file_utils, timing_utils, ratio_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'VOLUME','PCR']
FILENAME = 'daily_put_call_ratio'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

for tick in filenames:
    try:
        data = file_utils.get_history(tick)
        pcr = ratio_utils.get_put_call_ratio(tick)

        if math.isnan(pcr): continue

        if pcr < 0.5:
            tmp =  pd.DataFrame([[data.index[-1], 
                                    tick, 
                                    data['Close'].iloc[-1],
                                    data['Volume'].iloc[-1],
                                    pcr
                                    ]], columns=COLUMNS)

            df = pd.concat([df, tmp], ignore_index=True)
    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
