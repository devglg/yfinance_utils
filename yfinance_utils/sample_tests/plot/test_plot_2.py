#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#



import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import utils
import yfinance
import utils.list_util 
import utils.rsi_util
import utils.volume_util
import matplotlib.pyplot as plt

print("================================================================")
print("plot close volume and rsi")
print("================================================================")

COLUMNS = ["TICK","Close", "Volume", "rsi"]

tickers = utils.list_util.get_mag7()
figure, axis = plt.subplots(len(tickers),1)

for i in range(len(tickers)):
    t = yfinance.Ticker(tickers[i])

    df = pd.DataFrame(columns=COLUMNS)
    rsi = utils.rsi_util.get_rsi(t, period="1y", interval="1d")

    axis[i].plot(rsi["Close"], label="Price", color="tab:red")
    ax2 = axis[i].twinx()
    ax2.plot(rsi["Volume"], label="Volume", color="tab:green")
    ax3 = axis[i].twinx()
    ax3.plot(rsi["rsi"], label="rsi")
    
    axis[i].set_ylabel(tickers[i])


plt.grid()
plt.show()
