#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#



import warnings
warnings.filterwarnings("ignore")

import utils
import yfinance
import pprint
from lists.nasdaq100 import nasdaq100 as ticklist
import utils.rsi_util
import utils.volume_util

df_ticks = {}
counter = 0

t = yfinance.Tickers(ticklist)

for tick in ticklist:
    percent, average =  utils.volume_util.get_percent_volume(t.tickers[tick], period='1mo', days_back=2)
    if percent and average: 
        pprint.pprint(f"{t.tickers[tick].info['symbol']:6} volume is {percent:4}% from Average {average:13,}")




