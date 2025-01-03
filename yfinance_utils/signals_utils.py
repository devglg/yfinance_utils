#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
from finta import TA
import math
import yfinance
from yfinance_utils import constants

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

def is_stochastic_cross_up(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] > stochd.iloc[-1] \
           and stochk.iloc[-days_back] < stochd.iloc[-days_back] \
           and stochk.iloc[-1] > line and stochk.iloc[-days_back] < line

def is_stochastic_cross_down(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] < stochd.iloc[-1] \
           and stochk.iloc[-days_back] > stochd.iloc[-days_back] \
           and stochk.iloc[-1] < line and stochk.iloc[-days_back] > line

##########################
# SMA and EMA indicators #
##########################

def is_ma_bullish_trend(data, sma=30, ema=10, day=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return data['Close'].iloc[-day] > sma.iloc[-day] and data['Close'].iloc[-day] > ema.iloc[-day]

def is_ma_trend_reversing(data, sma=30, ema=10, day=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return data['Close'].iloc[-day] > ema.iloc[-day] and data['Close'].iloc[-day] < sma.iloc[-day]

def is_ma_cross_down(data, sma=30, ema=10, days=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return is_ma_bullish_trend(data, day=2) \
        and ema.iloc[-days] > sma.iloc[-days] \
        and ema.iloc[-1] < sma.iloc[-1]

def is_ma_cross_up(data, sma=30, ema=10, days=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return is_ma_bearish_trend(data, day=2) \
        and ema.iloc[-days] < sma.iloc[-days] \
        and ema.iloc[-1] > sma.iloc[-1]

def is_ma_bearish_trend(data, sma=30, ema=10, day=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return data['Close'].iloc[-day] < sma.iloc[-day] and data['Close'].iloc[-day] < ema.iloc[-day]

def is_ma_price_cross_down(data, sma=30, ema=10, day=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return is_ma_bullish_trend(data, day=2) \
        and data['Open'].iloc[-day] > ema.iloc[-day] \
        and data['Close'] < ema.iloc[-day]

def is_ma_price_cross_up(data, sma=30, ema=10, day=1):
    sma = TA.SMA(data, sma)
    ema = TA.EMA(data, ema)
    return is_ma_bearish_trend(data, day=2) \
        and data['Open'].iloc[-day] < ema.iloc[-day] \
        and data['Close'] > ema.iloc[-day]

##########################
# 52 week indicators     #
##########################

def is_price_year_low(data, pct_diff = 2):
    low = data['Close'].iloc[-constants.TRADING_DAYS_IN_YEAR:].min()
    return math.isclose(low, data['Close'].iloc[-1], abs_tol=(low * pct_diff / 100))

def is_price_year_high(data, pct_diff = 2):
    high = data['Close'].iloc[-constants.TRADING_DAYS_IN_YEAR:].max()
    return math.isclose(high, data['Close'].iloc[-1], abs_tol=(high * pct_diff / 100))

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
    t = yfinance.Ticker('VIX')
    data = t.download(period="1y")
    hma10 = TA.HMA(data, period=10) 
    hma20 = TA.HMA(data, period=20) 
    return hma10.iloc[-day] < hma20.iloc[-day] \
            and hma10.iloc[-1] > hma20.iloc[-1]

def is_vix_cross_down(day=2):
    t = yfinance.Ticker('VIX')
    data = t.download(period="1y")
    hma10 = TA.HMA(data, period=10) 
    hma20 = TA.HMA(data, period=20) 
    return hma10.iloc[-day] > hma20.iloc[-day] \
            and hma10.iloc[-1] < hma20.iloc[-1]

