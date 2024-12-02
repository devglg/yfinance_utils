#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import yfinance
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils
from yfinance_utils import volume_utils

print("================================================================")
print("plot close volume and rsi")
print("================================================================")

COLUMNS = ["TICK","Close", "Volume", "rsi"]

tickers = list_utils.get_mag7()

for tick in tickers:
    t = yfinance.Ticker(tick)

    df = pd.DataFrame(columns=COLUMNS)
    rsi = rsi_utils.get_rsi(t, period="1d", interval="1m")

    figure, ax1 = plt.subplots()
    ax1.plot(rsi["Close"], label="Price", color="tab:red")
    ax1.legend().set_loc(1)

    ax2 = ax1.twinx()
    ax2.plot(rsi["Volume"], label="Volume", color="tab:green")
    ax2.legend().set_loc(2)

    ax3 = ax1.twinx()
    ax3.plot(rsi["rsi"], label="rsi")
    ax3.legend().set_loc(9)

    plt.grid()
    plt.title(tick)
    plt.show()
