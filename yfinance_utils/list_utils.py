#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
#
import yfinance
import pandas as pd
from collections import Counter

from yfinance_utils.lists.mag7 import mag7
from yfinance_utils.lists.nasdaq100 import nasdaq100
from yfinance_utils.lists.snp500 import snp500
from yfinance_utils.lists.aero_def import aero_def as XAR
from yfinance_utils.lists.nasdaq import nasdaq
from yfinance_utils.lists.nyse import nyse
from yfinance_utils.lists.rus2000 import rus2000
from yfinance_utils.lists.remove import remove
from yfinance_utils.lists.adhoc import adhoc
from yfinance_utils.lists.ab import ab
from yfinance_utils.lists.dow import dow
from yfinance_utils.lists.main import markets
from yfinance_utils.lists.main import sectors

from yfinance_utils.lists.xlb_materials import XLB
from yfinance_utils.lists.xlc_comm import XLC
from yfinance_utils.lists.xle_energy import XLE
from yfinance_utils.lists.xlf_financials import XLF
from yfinance_utils.lists.xli_industrials import XLI
from yfinance_utils.lists.xlk_tech import XLK
from yfinance_utils.lists.xlp_staples import XLP
from yfinance_utils.lists.xlre_realestate import XLRE
from yfinance_utils.lists.xlu_utilities import XLU
from yfinance_utils.lists.xlv_healthcare import XLV
from yfinance_utils.lists.xly_discretionary import XLY

# this is to access sectors easily
SECTORS = {
    "XLB":XLB,
    "XLC":XLC,
    "XLE":XLE,
    "XLF":XLF,
    "XLI":XLI,
    "XLK":XLK,
    "XLP":XLP,
    "XLRE":XLRE,
    "XLU":XLU,
    "XLV":XLV,
    "XLY":XLY,
    "XAR":XAR
}

def remove_duplicate_values(my_dict):
    result = {}
    seen_values = set()

    for key, value in my_dict.items():
        if value not in seen_values:
            result[key] = value
            seen_values.add(value)

    return result

def get_all_symbols_from_sectors():
    all = {**XLB, **XLC, **XLE, **XLF, **XLI, **XLK, **XLP, **XLRE, **XLU, **XLV, **XLY, **XAR}
    all = remove_duplicate_values(all)
    keys = all.keys()
    return list(set(keys))

def get_discretionary():
    return list(set(XLY.keys()))

def get_health_care():
    return list(set(XLV.keys()))

def get_utilities():
    return list(set(XLU.keys()))

def get_real_estate():
    return list(set(XLRE.keys()))

def get_materials():
    return list(set(XLB.keys()))

def get_communication():
    return list(set(XLC.keys()))

def get_energy():
    return list(set(XLE.keys()))

def get_financials():
    return list(set(XLF.keys()))

def get_industrials():
    return list(set(XLI.keys()))

def get_technology():
    return list(set(XLK.keys()))

def get_staples():
    return list(set(XLP.keys()))

def get_all_tickers():
    all = mag7 + nasdaq100 + snp500 + XAR + nasdaq + nyse + rus2000 + adhoc + ab + dow
    return list(set(all) - set(remove))

def get_rus2000():
    return list(set(rus2000) - set(remove))

def get_aero_def():
    return list(set(XAR) - set(remove))

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

def get_ab():
    return list(set(ab + list(markets.keys()) + list(sectors.keys())))

def get_dow():
    return list(set(dow))

def get_markets():
    return list(set(markets.keys()))

def get_sectors():
    return list(set(sectors.keys()))

def get_top_performers(symbols, size=3, days=30):
    COLUMNS = ['Adj Close', 'Open','High','Low','Close','Volume']
    data = yfinance.download(symbols, period='1y')
    symlist = {}
    for symbol in symbols:
        _df = pd.DataFrame()
        _df = data.loc[:,(slice(None),symbol)]
        _df.columns = COLUMNS
        _df.reset_index(inplace=True)
        _df = _df[-30:]
        temp_1 = _df['Close'].iloc[-1]
        temp_2 = _df['Close'].iloc[-days]
        pct = round(((temp_1 - temp_2) / temp_2 * 100),2)
        symlist[symbol] = pct

    k = Counter(symlist)
    top = k.most_common(size)
    return  top