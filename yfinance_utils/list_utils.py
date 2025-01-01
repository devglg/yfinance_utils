#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
#

from yfinance_utils.lists.mag7 import mag7
from yfinance_utils.lists.nasdaq100 import nasdaq100
from yfinance_utils.lists.snp500 import snp500
from yfinance_utils.lists.aero_def import aero_def
from yfinance_utils.lists.nasdaq import nasdaq
from yfinance_utils.lists.nyse import nyse
from yfinance_utils.lists.rus2000 import rus2000
from yfinance_utils.lists.remove import remove
from yfinance_utils.lists.adhoc import adhoc

def get_all_tickers():
    all = mag7 + nasdaq100 + snp500 + aero_def + nasdaq + nyse + rus2000 + adhoc
    return list(set(all) - set(remove))

def get_rus2000():
    return list(set(rus2000) - set(remove))

def get_aero_def():
    return list(set(aero_def) - set(remove))

def get_mag7():
    return list(set(mag7) - set(remove))

def get_snp500():
    return list(set(snp500) - set(remove))

def get_nasdaq100():
    return list(set(nasdaq100) - set(remove))

def get_nasdaq():
    return list(set(nasdaq) - set(remove))

def get_adhoc():
    return list(set(adhoc) - set(remove))