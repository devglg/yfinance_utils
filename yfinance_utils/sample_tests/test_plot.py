#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import yfinance
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils

ticklist = list_utils.get_mag7()

df_ticks = {}
counter = 0

t = yfinance.Tickers(ticklist)

for tick in t.tickers:
    df = rsi_utils.get_rsi(t.tickers[tick])
    df_ticks[tick] = df

figure, axis = plt.subplots(len(df_ticks), 1)

for i in range(len(df_ticks)):
    axis[i].plot(df_ticks[ticklist[i]]["Low"])
    axis[i].plot(df_ticks[ticklist[i]]["High"])
    axis[i].plot(df_ticks[ticklist[i]]["Close"])
    axis[i].set_ylabel(ticklist[i])

plt.grid(True)
plt.show()



