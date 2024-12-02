#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings("ignore")

import yfinance
from yfinance_utils import list_utils 
from yfinance_utils import rsi_utils
from yfinance_utils import volume_utils


ticker_list = list_utils.get_mag7()
t = yfinance.Tickers(ticker_list)

print("===============================================================================")

for tick in ticker_list:
    x = t.tickers[tick]
    data = list(rsi_utils.get_rsi(x)["rsi"])
    rsi = data[-1]
    avg_vol =  x.info["averageVolume"]
    vol_info = x.info['volume']
    price = x.info["currentPrice"]
    print(f"{tick:6} price: {price:8,}   rsi: {rsi:6,.2f}   vol: {vol_info:12,}   avg: {avg_vol:11,}")

print("===============================================================================")

