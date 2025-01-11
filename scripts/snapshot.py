#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import time
import pandas as pd
import yfinance
from datetime import date, timedelta
from yfinance import Ticker
from yfinance_utils import list_utils, timing_utils, file_utils, constants

thirteen_months = str(date.today() - timedelta(weeks=60))
oneyearago = str(date.today() - timedelta(weeks=52))
today=str(date.today())
tomorrow=str(date.today() + timedelta(days=1))

start_date = thirteen_months # get 60 weeks to have complete SMA
end_date = tomorrow 
interval = '1d'


# get only the important symbols. this is more than enough
symbol_list = list_utils.get_nasdaq100() \
            + list_utils.get_adhoc() \
            + list_utils.get_ab() \
            + list_utils.get_snp500() \
            + list_utils.get_dow() \
            + list_utils.get_all_symbols_from_sectors()
# remove dups
symbol_list = list(set(symbol_list))

# start the timer
start_time = timing_utils.start(symbol_list, 'snapshot', f'getting historic data from: {start_date} to: {end_date}')

if len(symbol_list) > 600:
    COLUMNS = ['Open','High','Low','Close','Volume']
    # long list download one by one and pause in between to it doesn't kill the connection
    for symbol in symbol_list:
        try:
            tmp = Ticker(symbol)
            data = tmp.history(start=start_date, end=end_date, rounding=True, timeout=20, actions=False, interval=interval)
            data.columns = COLUMNS
            if data['Close'].iloc[-1] > constants.MINIMUM_PRICE:
                file_utils.save_historic_data(data, symbol)  
            time.sleep(.5)
        except Exception as e:
            pass

else:
    # shorter list download all at once
    COLUMNS = ['Adj Close', 'Open','High','Low','Close','Volume']
    data = yfinance.download(symbol_list, start=start_date, end=end_date, rounding=True, interval=interval)
    for symbol in symbol_list:
        try:
            tdata = pd.DataFrame()
            tdata = data.loc[:,(slice(None),symbol)]
            tdata.columns = COLUMNS
            if tdata['Close'].iloc[-1] > constants.MINIMUM_PRICE:
                file_utils.save_historic_data(tdata, symbol)
        except Exception as e:
            continue

timing_utils.end(start_time, 'snapshot', f'data downloaded and saved')
    