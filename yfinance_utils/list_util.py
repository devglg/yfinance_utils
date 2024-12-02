#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
#

from lists.mag7 import mag7
from lists.nasdaq100 import nasdaq100
from lists.snp500 import snp500
from lists.aero_def import aero_def

def get_all_tickers():
    all = mag7 + nasdaq100 + snp500 + aero_def
    return list(set(all))

def get_aero_def():
    return list(set(aero_def))

def get_mag7():
    return list(set(mag7))

def get_snp500():
    return list(set(snp500))

def get_nasdaq100():
    return list(set(nasdaq100))
