#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Zack West
# This code was written by zack west and can be found here:
# https://www.alpharithms.com/relative-strength-index-rsi-in-python-470209/
#

import warnings
warnings.filterwarnings("ignore")

import pandas as pd

def get_mfi(data, window_length=14):
    """
    get mfi from the data
    lookback = number of days to use to calculate the rsi
    returns data frame with price OHLC including rsi
    """
    df = pd.DataFrame()

    if window_length > len(data):
        return None

    df["typical"] = (data["High"] + data["Low"] + data["Close"]) / 3
    df['raw'] = df['typical'] * data['Volume']
    
    df['diff'] = df["raw"].diff(1)
    df['pos'] = df['diff'].clip(lower=0).round(2)
    df['neg'] = df['diff'].clip(upper=0).abs().round(2)

    df['avg_pos'] = df['pos'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    df['avg_neg'] = df['neg'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]

    # Average posittive
    for i, row in enumerate(df['avg_pos'].iloc[window_length+1:]):
        df['avg_pos'].iloc[i + window_length + 1] =\
        (df['avg_pos'].iloc[i + window_length] * (window_length - 1) + df['pos'].iloc[i + window_length + 1]) / window_length

    # Average negative
    for i, row in enumerate(df['avg_neg'].iloc[window_length+1:]):
        df['avg_neg'].iloc[i + window_length + 1] =\
        (df['avg_neg'].iloc[i + window_length] * (window_length - 1) + df['neg'].iloc[i + window_length + 1]) / window_length

    df['mf'] = df['avg_pos'] / df['avg_neg']
    df['mfi'] = 100 - (100 / (1.0 + df['mf']))

    data['mfi'] = df['mfi']
    return data

