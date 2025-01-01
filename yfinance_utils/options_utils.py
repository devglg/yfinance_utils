#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
# 
import math

def get_all_options(t):
    options = t.option_chain()
    return options.calls + options.puts

def get_calls(t):
    options = t.option_chain()
    return options.calls

def get_calls_volume(t):
    options = t.option_chain()
    volume = list(options.calls['volume'])
    return sum(x for x in volume if not math.isnan(x))

def get_puts(t):
    options = t.option_chain()
    return options.puts

def get_puts_volume(t):
    options = t.option_chain()
    volume = list(options.puts['volume'])
    return sum(x for x in volume if not math.isnan(x))
