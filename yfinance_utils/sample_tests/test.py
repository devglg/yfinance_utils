#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings("ignore")

import statistics
import yfinance
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils
from yfinance_utils import volume_utils

ticker_list = [
    "PRZO",
    "PASG",
    "EPOW",
    "PGHL",
    "TDTH",
    "DPRO",
    "SATL",
    "MDAI",
    "HURA",
    "ATHE",
    "NTRP",
    "DBVT",
    "RGTI",
    "RCAT",
    "CABA",
    "LQR",
    "PNBK",
    "IFBD",
    "MOB",
    "DSY",
    "MOBX",
    "BGM",
    "ANTX",
    "STCN",
    "SDOT",
    "HDL",
    "PDYN",
    "GRRR",
    "OTLK",
    "AISP"
]
t = yfinance.Tickers(ticker_list)

print("===========================================================================================================================")
print(f"tick  | last2   | last1   | up %        | vol_avg     | vol2        | vol1        | rsi2    | rsi1    | mean%   | median% |")

for tick in ticker_list:
    x = t.tickers[tick]
    rsi = rsi_utils.get_rsi(x, period= "1y", interval="1d")
    if rsi is None:
        continue
    
    avg = statistics.mean(list(rsi["Close"]))
    med = statistics.median(list(rsi["Close"]))
    avg_vol = statistics.mean(list(rsi["Volume"]))


    vol2 = rsi["Volume"].iloc[-2]
    vol1 = rsi["Volume"].iloc[-1]
    last2 = rsi["Close"].iloc[-2]
    last1 = rsi["Close"].iloc[-1]
    rsi2 = rsi["rsi"].iloc[-2]
    rsi1 = rsi["rsi"].iloc[-1]


    # print(f"{tick:6}:last2:{last2:9,.2f} :last1: {last1:9,.2f}: up % :{last1 / last2 * 100:12,.2f}:vol_avg:{avg_vol:13,.2f}: vol2:{vol2 / avg_vol * 100:13,.2f}: vol1:{vol1 / avg_vol * 100:13,.2f}: rsi2:{rsi2:9,.2f}: rsi1:{rsi1:9,.2f}: mean%: {last1/avg*100:9,.2f}: median%: {last1/med*100:9,.2f}: ")
    print(f"{tick:6}|{last2:9,.2f}|{last1:9,.2f}| {last1 / last2 * 100:12,.2f}|{avg_vol:13,.2f}|{vol2 / avg_vol * 100:13,.2f}|{vol1 / avg_vol * 100:13,.2f}|{rsi2:9,.2f}|{rsi1:9,.2f}|{last1/avg*100:9,.2f}|{last1/med*100:9,.2f}| ")

print("===========================================================================================================================")

