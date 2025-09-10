#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
import math
from yfinance_utils import file_utils as file_utils


def get_price_intervals_rising(tick):
    data = file_utils.get_history(tick)
    c = list(data['Close'])
    for i in range(len(c)-1, 2, -1):
        if c[i-1] < c[i]:
            continue
        else:
            return(len(c) - i)

# day1 and day2 is days ago in number
def is_gap_up(data, day1=3, day2=2):
    close1 = data['Close'].iloc[-day1]
    open2 = data['Open'].iloc[-day2]
    return open2 > close1

# day is days ago in number
def is_close_high(data, tol=1, day=2):
    close = data['Close'].iloc[-day]
    high = data['High'].iloc[-day]
    tolerance = high * tol / 100
    return math.isclose(close, high, rel_tol=tolerance)


