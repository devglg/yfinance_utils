#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#



import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import utils
import yfinance
import utils.list_util 
import utils.rsi_util
import utils.volume_util

TEN_MILLION = 10000000

ticker_list = utils.list_util.get_all_tickers()
t = yfinance.Tickers(ticker_list)

print("================================================================")
print("Getting today's volume higher than x")
print("================================================================")

COLUMNS = ["TICK","VOLUME", "AVG", "RSI"]
df = pd.DataFrame(columns=COLUMNS)

for tick in ticker_list:
    x = t.tickers[tick]
    avg_vol =  x.info["averageVolume"]
    vol_info = x.info['volume']

    rsi = utils.rsi_util.get_rsi(x)
    rsix = round(rsi["rsi"].iloc[len(rsi) - 1], 2)
    pct = vol_info / avg_vol * 100

    if pct > 100.0 and vol_info > TEN_MILLION:
        temp = pd.DataFrame([[tick,vol_info,avg_vol,rsix]], columns=COLUMNS)
        df = pd.concat([df,temp])
print(df)
