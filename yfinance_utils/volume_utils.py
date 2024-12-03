#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import statistics

def get_percent_volume(ticker, period='1mo', days_back=0):
    """
        period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        using more than 6mo may be useless

        day = day to check against average. starts today and goes back

        returns the percentage of volume / average for the period
    """

    data = ticker.history(period = period)
    volume = data["Volume"].iloc[len(data)-days_back]
    average = statistics.mean(data["Volume"])
    median = statistics.median(data["Volume"])
    percentage = int(((volume/average)-1)*100)
    return {"volume":volume, "percentage":percentage, "average":average, "median": median}
