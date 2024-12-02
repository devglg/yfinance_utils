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

ticklist = list_utils.get_nasdaq100()

t = yfinance.Tickers(ticklist)

for tick in t.tickers:
    df = rsi_utils.get_rsi(t.tickers[tick])
    print(f"{tick}: {df}")
    print("-----------------------------------------------------------------------")
    