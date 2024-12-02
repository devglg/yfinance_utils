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




