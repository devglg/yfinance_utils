#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
from finta import TA
import math


def is_macd_cross_up(data, days_back = 5, line = 10):
    macd = TA.MACD(data)

    return macd['MACD'].iloc[-1] > macd['SIGNAL'].iloc[-1] \
           and macd['MACD'].iloc[-days_back] < macd['SIGNAL'].iloc[-days_back] \
           and macd['MACD'].iloc[-1] < line

def is_macd_cross_down(data, days_back = 5, line = -10):
    macd = TA.MACD(data)
    return macd['MACD'].iloc[-1] < macd['SIGNAL'].iloc[-1] \
           and macd['MACD'].iloc[-days_back] > macd['SIGNAL'].iloc[-days_back] \
           and macd['MACD'].iloc[-1] > line

def is_stoch_cross_up(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] > stochd.iloc[-1] \
           and stochk.iloc[-days_back] < stochd.iloc[-days_back] \
           and stochk.iloc[-1] > line and stochk.iloc[-days_back] < line

def is_stoch_cross_down(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] < stochd.iloc[-1] \
           and stochk.iloc[-days_back] > stochd.iloc[-days_back] \
           and stochk.iloc[-1] < line and stochk.iloc[-days_back] > line

def is_upward_trend(data, days = 50):
    ma = TA.EMA(data, days)
    return data['Close'].iloc[-1] > ma.iloc[-1]

def is_downward_trend(data, days = 50):
    ma = TA.EMA(data, days)
    return data['Close'].iloc[-1] < ma.iloc[-1]

def is_52wk_low(data, pct_diff = 2):
    low = data['Close'].min()
    return math.isclose(low, data['Close'].iloc[-1], abs_tol=(low * pct_diff / 100))

def is_52wk_high(data, pct_diff = 2):
    high = data['Close'].max()
    return math.isclose(high, data['Close'].iloc[-1], abs_tol=(high * pct_diff / 100))