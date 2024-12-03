#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import yfinance
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils
from yfinance_utils import volume_utils

TEN_MILLION = 10000000

ticker_list = list_utils.get_all_tickers()
t = yfinance.Tickers(ticker_list)

print("================================================================")
print("Getting today's volume higher than x")
print("================================================================")

COLUMNS = ["TICK","VOLUME", "AVG", "RSI"]
df = pd.DataFrame(columns=COLUMNS)

for tick in ticker_list:
    x = t.tickers[tick]
    avg_vol =  x.info["averageVolume"] or 0
    vol_info = x.info['volume'] or 0

    rsi = rsi_utils.get_rsi(x)
    rsix = round(rsi["rsi"].iloc[-1], 2)
    pct = vol_info / avg_vol * 100

    if pct > 100.0 and vol_info > TEN_MILLION:
        temp = pd.DataFrame([[tick,vol_info,avg_vol,rsix]], columns=COLUMNS)
        df = pd.concat([df,temp])
print(df)
