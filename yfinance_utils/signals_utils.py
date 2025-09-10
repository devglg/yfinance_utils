#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
from finta import TA
import math
import pandas as pd
from yfinance_utils import constants, file_utils

##########################
# MACD indicators        #
##########################

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

##########################
# STOCHASTIC indicators  #
##########################

def is_stochastic_cross_up(data, days_back = 2, line = 30):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] > stochd.iloc[-1] \
           and stochk.iloc[-days_back] < stochd.iloc[-days_back] \
           and stochk.iloc[-1] < line

def is_stochastic_cross_down(data, days_back = 2, line = 70):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] < stochd.iloc[-1] \
           and stochk.iloc[-days_back] > stochd.iloc[-days_back] \
           and stochk.iloc[-1] > line

##########################
# SMA and EMA indicators #
##########################

def is_ma_bullish_trend(data, sma=30, ema=10, day=1):
    slow = TA.SMA(data, sma)
    fast = TA.EMA(data, ema)
    return data['Close'].iloc[-day] > slow.iloc[-day] and data['Close'].iloc[-day] > fast.iloc[-day]

def is_ma_bearish_trend(data, sma=30, ema=10, day=1):
    slow = TA.SMA(data, sma)
    fast = TA.EMA(data, ema)
    return data['Close'].iloc[-day] < slow.iloc[-day] and data['Close'].iloc[-day] < fast.iloc[-day]

def is_ma_trend_reversing(data, sma=30, ema=10, day=1):
    slow = TA.SMA(data, sma)
    fast = TA.EMA(data, ema)
    return data['Close'].iloc[-day] > fast.iloc[-day] and data['Close'].iloc[-day] < slow.iloc[-day]

def is_ma_cross_down(data, sma=30, ema=10):
    return is_ma_bullish_trend(data, sma=sma, ema=ema, day=5) \
        and is_ma_bearish_trend(data, sma=sma, ema=ema, day=1)

def is_ma_cross_up(data, sma=30, ema=10):
    return is_ma_bearish_trend(data, sma=sma, ema=ema, day=5) \
        and is_ma_bullish_trend(data, sma=sma, ema=ema, day=1)

def is_ma_price_cross_down(data, ma='ema', ma_days=10, day=2):
    xma = pd.DataFrame()
    if 'e' in ma:
        xma = TA.EMA(data, ma_days)
    else:
        xma = TA.SMA(data, ma_days)
        
    return data['Open'].iloc[-day] > xma.iloc[-day] \
        and data['Close'].iloc[-day] < xma.iloc[-day]

def is_ma_price_cross_up(data, ma='ema', ma_days=10, day=2):
    xma = pd.DataFrame()
    if 'e' in ma:
        xma = TA.EMA(data, ma_days)
    else:
        xma = TA.SMA(data, ma_days)
        
    return data['Open'].iloc[-day] < xma.iloc[-day] \
        and data['Close'].iloc[-day] > xma.iloc[-day]


##########################
# 52 week indicators     #
##########################

def get_price_year_low(data):
    return data['Close'].iloc[-constants.TRADING_DAYS_IN_YEAR:].min()

def is_price_year_low(data, precision = 2):
    low = get_price_year_low(data)
    return math.isclose(low, data['Close'].iloc[-1], abs_tol=(low * precision / 100))

def get_price_year_high(data):
    return data['Close'].iloc[-constants.TRADING_DAYS_IN_YEAR:].max()

def is_price_year_high(data, precision = 2):
    high = get_price_year_high(data)
    return math.isclose(high, data['Close'].iloc[-1], abs_tol=(high * precision / 100))

##########################
# RSI indicators         #
##########################

def is_rsi_oversold(data, period=14, line=30):
    rsi = TA.RSI(data,period)
    return rsi.iloc[-1] < line

def is_rsi_overbough(data, period=14, line=70):
    rsi = TA.RSI(data,period)
    return rsi.iloc[-1] > line

def is_rsi_year_low(data, period=14):
    rsi = TA.RSI(data.iloc[-constants.TRADING_DAYS_IN_YEAR], period)
    return math.isclose(rsi.iloc[-1], rsi.min(), abs_tol=2)

def is_rsi_year_high(data, period=14):
    rsi = TA.RSI(data.iloc[-constants.TRADING_DAYS_IN_YEAR:], period)
    return math.isclose(rsi.iloc[-1], rsi.max(), abs_tol=2)

##########################
# IV indicators          #
##########################

def is_vix_cross_up(day=2):
    data = file_utils.get_historic_data('^VIX')
    fast = TA.HMA(data, period=10) 
    slow = TA.HMA(data, period=20) 
    return fast.iloc[-day] < slow.iloc[-day] \
            and fast.iloc[-1] > slow.iloc[-1]

def is_vix_cross_down(day=2):
    data = file_utils.get_historic_data('^VIX')
    fast = TA.HMA(data, period=10) 
    slow = TA.HMA(data, period=20) 
    return fast.iloc[-day] > slow.iloc[-day] \
            and fast.iloc[-1] < slow.iloc[-1]

def is_vix_trending_up():
    data = file_utils.get_historic_data('^VIX')
    fast = TA.HMA(data, period=10) 
    slow = TA.HMA(data, period=20) 
    return fast.iloc[-1] > slow.iloc[-1]

#####################################
# SUPPORT and RESISTANCE indicators #
#####################################

def is_resistance_breake_up(data, days=14, min_fails = 3, pct_res = 0.5, pct_break = 3):
    d = data['High'][-days:-2]
    today = data['Close'][-1]

    d_max = d.max()
    d_max_pct = d_max * pct_res / 100
    d_break = d_max + (d_max * pct_break / 100)

    counter = 0
    for i in d:
        if math.isclose(i, d_max, abs_tol=d_max_pct):
            counter = counter + 1
    
    if counter > min_fails and today > d_break:
        return True
    else:
        return False
    
def is_support_breake_down(data, days=14, min_fails = 3, pct_res=0.5, pct_break = 3):
    d = data['Low'][-days:-2]
    today = data['Close'][-1]

    d_min = d.min()
    d_min_pct = d_min * pct_res / 100
    d_break = d_min + (d_min * pct_break / 100)

    counter = 0
    for i in d:
        if math.isclose(i, d_min, abs_tol=d_min_pct):
            counter = counter + 1
    
    if counter > min_fails and today < d_break:
        return True
    else:
        return False
    
##########################
# CAHOLD indicators      #
##########################

def is_cahold(data, days=5):
    d = data[-days:]
    d['IS_RED'] = d['Close'] < d['Open']
    if bool(d['IS_RED'].iloc[-1]): return False
    for i in range(-days,-1,-1):
        if not bool(d['IS_RED'].iloc[i]):
            return d['Close'].iloc[-1] > d['High'].iloc[i]
    return False

def is_cblohd(data, days=4):
    d = data[-days:]
    d['IS_GREEN'] = d['Close'] > d['Open']
    if bool(d['IS_GREEN'].iloc[-1]): return False
    for i in range(-2, -days,-1):
        if bool(d['IS_GREEN'].iloc[i]):
            return d['Close'].iloc[-1] < d['Low'].iloc[i]
    return False

##########################
# VOLUME indicators      #
##########################

def is_high_volume(data, pct_higher = 30):
    d = data[-constants.TRADING_DAYS_IN_YEAR:]
    d_avg = d['Volume'].mean()
    d_high_vol = d_avg + (d_avg * pct_higher / 100)
    return d['Volume'].iloc[-1] > d_high_vol