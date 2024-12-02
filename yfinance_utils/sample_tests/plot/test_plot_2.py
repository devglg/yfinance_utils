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
