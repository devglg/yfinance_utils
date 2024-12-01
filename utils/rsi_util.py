#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Zack West
# This code was written by zack west and can be found here:
# https://www.alpharithms.com/relative-strength-index-rsi-in-python-470209/
#




import utils.constants as const
import pandas as pd


def get_rsi(ticker, window_length=14, period="1mo", interval="1d"):
    """
    get rsi from the data
    lookback = number of days to use to calculate the rsi
    returns data frame with price history including rsi
    """
    df = pd.DataFrame()
    try:
        data = ticker.history(period=period, interval=interval)
    except Exception:
        return None

    if window_length > len(data):
        print(f"{ticker.info['symbol']} does not have enough data. window length {window_length} data items {len(data)}")
        return None

    df['diff'] = data["Close"].diff(1)
    df['gain'] = df['diff'].clip(lower=0).round(2)
    df['loss'] = df['diff'].clip(upper=0).abs().round(2)

    df['avg_gain'] = df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    df['avg_loss'] = df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]

    # Average Gains
    for i, row in enumerate(df['avg_gain'].iloc[window_length+1:]):
        df['avg_gain'].iloc[i + window_length + 1] =\
        (df['avg_gain'].iloc[i + window_length] * (window_length - 1) + df['gain'].iloc[i + window_length + 1]) / window_length

    # Average Losses
    for i, row in enumerate(df['avg_loss'].iloc[window_length+1:]):
        df['avg_loss'].iloc[i + window_length + 1] =\
        (df['avg_loss'].iloc[i + window_length] * (window_length - 1) + df['loss'].iloc[i + window_length + 1]) / window_length

    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1.0 + df['rs']))

    data['rsi'] = df['rsi']
    return data

