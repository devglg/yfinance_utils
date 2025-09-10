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

DOWNLOAD_HISTORY = False
DOWNLOAD_FINANCIALS = True

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
# start_time = timing_utils.start(symbol_list, 'snapshot', f'getting historic data from: {start_date} to: {end_date}')



if DOWNLOAD_HISTORY:
    if len(symbol_list) > 800:
        COLUMNS = ['Open','High','Low','Close','Volume']
        # long list download one by one and pause in between to it doesn't kill the connection
        for symbol in symbol_list:
            try:
                tmp = Ticker(symbol)
                data = tmp.history(start=start_date, end=end_date, rounding=True, timeout=20, actions=False, interval=interval, auto_adjust=False)
                data.columns = COLUMNS
                if data['Close'].iloc[-1] > constants.MINIMUM_PRICE:
                    file_utils.save_historic_data(data, symbol)  
                time.sleep(.5)
            except Exception as e:
                print(f'error on retrieving {symbol} history')
                continue

    else:
        # shorter list download all history at once
        COLUMNS = ['Adj Close', 'Open','High','Low','Close','Volume']
        data = yfinance.download(symbol_list, start=start_date, end=end_date, rounding=True, interval=interval, auto_adjust=False)
        for symbol in symbol_list:
            try:
                tdata = pd.DataFrame()
                tdata = data.loc[:,(slice(None),symbol)]
                tdata.columns = COLUMNS
                if tdata['Close'].iloc[-1] > constants.MINIMUM_PRICE:
                    file_utils.save_historic_data(tdata, symbol)
            except Exception as e:
                print(f'error retrieving {symbol} history')
                continue

if DOWNLOAD_FINANCIALS:
    for symbol in symbol_list:        
        try:
            file_utils.download_info(symbol)
        except Exception as e:
            print(f'error downloading {symbol} INFO')
            pass

        try:
            file_utils.download_income_statement(symbol)
        except Exception as e:
            print(f'error downloading {symbol} IS')
            pass

        try:
            file_utils.download_balance_sheet(symbol)
        except Exception as e:
            print(f'error downloading {symbol} BS')
            pass

        try:    
            file_utils.download_cashflow(symbol)
        except Exception as e:
            print(f'error downloading {symbol} CF')
            pass

        try:    
            file_utils.download_ratings(symbol)
        except Exception as e:
            print(f'error downloading {symbol} RT')
            pass

        try:    
            file_utils.download_analysts(symbol)
        except Exception as e:
            print(f'error downloading {symbol} ANALYSTS')
            pass

        try:    
            file_utils.download_news(symbol)
        except Exception as e:
            print(f'error downloading {symbol} NEWS')
            pass


# timing_utils.end(start_time, 'snapshot', f'data downloaded and saved')
    