#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# output to daily ETF volume file

# change directory to root of project
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parent2 = os.path.dirname(parent)
sys.path.append(parent2)

import warnings
warnings.filterwarnings("ignore")

import datetime
import statistics

import pandas as pd
import yfinance
import utils.list_util 
import utils.volume_util

HEADERS = ["VOLUME", "AVERAGE", "MEDIAN"]
dfnas = pd.DataFrame(HEADERS)
dfsnp = pd.DataFrame(HEADERS)

tickers_nq = yfinance.Tickers(utils.list_util.get_nasdaq100())
tickers_snp = yfinance.Tickers(utils.list_util.get_snp500())

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

