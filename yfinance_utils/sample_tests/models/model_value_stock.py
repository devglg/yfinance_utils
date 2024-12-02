#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#


import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import yfinance 
from yfinance_utils import list_utils
from yfinance_utils import model_utils as mu

MAX_PRICE_TO_SALES = 1.00
MAX_PRICE_TO_EARNINGS = 20.00

ticklist = list_utils.get_all_tickers()

t = yfinance.Tickers(ticklist)
companies = mu.get_sacks_value_stocks(t, max_price_to_earnings=MAX_PRICE_TO_EARNINGS, max_price_to_sales=MAX_PRICE_TO_SALES)
print(companies)
