#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

# output to daily ETF volume file

import warnings
warnings.filterwarnings("ignore")

import datetime
import statistics

import pandas as pd
import yfinance
from yfinance_utils import list_utils
from yfinance_utils import volume_utils

HEADERS = ["VOLUME", "AVERAGE", "MEDIAN"]
dfnas = pd.DataFrame(HEADERS)
dfsnp = pd.DataFrame(HEADERS)

tickers_nq = yfinance.Tickers(list_utils.get_nasdaq100())
tickers_snp = yfinance.Tickers(list_utils.get_snp500())

print(f"ETF, VOLUME, AVG, MEDIAN")

for t in tickers_nq.tickers:
    n =  tickers_nq.tickers[t].history()
    temp = pd.DataFrame([[n["Volume"].iloc[len(t)-1], statistics.mean(n["Volume"]), statistics.median(n["Volume"])]], columns=HEADERS)
    dfnas = pd.concat([dfnas, temp], ignore_index=True)

for t in tickers_snp.tickers:
    s =  tickers_snp.tickers[t].history()
    temp = pd.DataFrame([[s["Volume"].iloc[len(t)-1], statistics.mean(s["Volume"]), statistics.median(s["Volume"])]], columns=HEADERS)
    dfsnp = pd.concat([dfsnp, temp], ignore_index=True)

print(f"Nasdaq 100:{int(dfnas["VOLUME"].mean())}:{int(dfnas["AVERAGE"].mean())}:{int(dfnas["MEDIAN"].mean())}")
print(f"S&P 500:{int(dfsnp["VOLUME"].mean())}:{int(dfsnp["AVERAGE"].mean())}:{int(dfsnp["MEDIAN"].mean())}")

with open("daily_etf_volume.csv", "a", newline="") as f:
    print(f"{datetime.date.today()},Nasdaq 100,{int(dfnas["VOLUME"].mean())},{int(dfnas["AVERAGE"].mean())},{int(dfnas["MEDIAN"].mean())}", file=f)
    print(f"{datetime.date.today()},S&P 500,{int(dfsnp["VOLUME"].mean())},{int(dfsnp["AVERAGE"].mean())},{int(dfsnp["MEDIAN"].mean())}", file=f)

