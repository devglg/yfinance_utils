#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
# 
import math
from yfinance_utils import file_utils

def get_all_options(t):
    return get_puts_volume(t) + get_calls_volume(t)

def get_calls_volume(t):
    volume = file_utils.get_options(t)['calls']
    return volume

def get_puts_volume(t):
    volume = file_utils.get_options(t)['puts']
    return volume

def get_put_call_ration(t):
    return get_puts_volume(t) / get_calls_volume(t)