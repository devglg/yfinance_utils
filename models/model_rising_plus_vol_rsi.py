#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#


# change directory to root of project
import sys
import os
import math
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parent2 = os.path.dirname(parent)
sys.path.append(parent2)

# remove warnings
import warnings
warnings.filterwarnings("ignore")

# imports
from datetime import date
import statistics
import pandas as pd
import yfinance

import rsi_util

# local variables
WEEKS_RISING = 5
df = pd.DataFrame()
t = yfinance.Tickers(utils.list_util.get_all_tickers())
# t = yfinance.Tickers(["GS", "SOFI", "FDS", "C"])

print(str(date.today()))
print("================================================================")
print(f"Getting tranding up by CLOSE price for {WEEKS_RISING} weeks")

ticker_list = []
weeks_list = []
for tick in  t.tickers:
    c = list(t.tickers[tick].history(period = "3mo", interval = "1wk")["Close"])
    for i in range(len(c)-1, 2, -1):
        if c[i-1] < c[i]:
            continue
        else:
            if (len(c) - i) > WEEKS_RISING:
                ticker_list.append(tick)
                weeks_list.append(len(c) - i)
            break
df["ticker"] = ticker_list
df["weeks"] = weeks_list

print("================================================================")
print("Getting rsi")

rsi_list = []
for tick in df["ticker"]:
    r = utils.rsi_util.get_rsi(t.tickers[tick], period="1y")
    if r is None:
        continue
    else:
        rsi_list.append(r["rsi"].iloc[len(r)-1])

df["rsi"] = rsi_list
df = df.dropna(subset="rsi")

print("================================================================")
print("Getting volume")

volume_list_1 = []
volume_list_2 = []
vol_avg_list = []
for tick in df["ticker"]:
    d = t.tickers[tick].history()
    volume_list_1.append(d["Volume"].iloc[len(d)-1])
    volume_list_2.append(d["Volume"].iloc[len(d)-2])
    vol_avg_list.append(statistics.mean(d["Volume"]))
df["vol_average"] = vol_avg_list
df["volume_last_day"] = volume_list_1
df["volume_two_days_ago"] = volume_list_2

print("================================================================")
print("Creating file")

df["vol_change"] = df["volume_last_day"].sub(df["volume_two_days_ago"], axis=0) / df["volume_last_day"]
df.round(2).sort_values(by=["ticker"]).to_csv(f"rising_plus_vol_rsi_{str(date.today())}.csv", index=False)
