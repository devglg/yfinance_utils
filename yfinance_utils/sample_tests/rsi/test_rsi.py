#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#



import warnings
warnings.filterwarnings("ignore")

import utils
import yfinance
from lists.nasdaq100 import nasdaq100 as ticklist
import utils.rsi_util
import utils.volume_util

df_ticks = {}
counter = 0

t = yfinance.Tickers(ticklist)

for tick in t.tickers:
    df = utils.rsi_util.get_rsi(t.tickers[tick])
    print(f"{tick}: {df}")
    print("-----------------------------------------------------------------------")
    