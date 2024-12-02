#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#



import warnings
warnings.filterwarnings("ignore")

import utils
import yfinance
import utils.list_util 
import utils.rsi_util
import utils.volume_util


ticker_list = utils.list_util.positions
t = yfinance.Tickers(ticker_list)

print("===============================================================================")

for tick in ticker_list:
    x = t.tickers[tick]
    data = list(utils.rsi_util.get_rsi(x)["rsi"])
    rsi = data[-1]
    avg_vol =  x.info["averageVolume"]
    vol_info = x.info['volume']
    price = x.info["currentPrice"]
    print(f"{tick:6} price: {price:8,}   rsi: {rsi:6,.2f}   vol: {vol_info:12,}   avg: {avg_vol:11,}")

print("===============================================================================")

