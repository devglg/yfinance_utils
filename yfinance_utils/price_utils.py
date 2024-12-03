#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

def get_number_intervals_rising(tick, period = "3mo", interval = "1wk"):
    c = list(tick.history(period = period, interval = interval)["Close"])
    for i in range(len(c)-1, 2, -1):
        if c[i-1] < c[i]:
            continue
        else:
            return(len(c) - (i + 1))
