import os
import pandas as pd
from datetime import date, timedelta
import yfinance as yf
from yfinance_utils import list_utils, timing_utils, file_utils

COLUMNS = ['Adj Close','Close','High','Low','Open','Volume']

today=str(date.today())
oneyearago = str(date.today() - timedelta(weeks=52))
twoyearsago = str(date.today() - timedelta(weeks=104))
start_date = twoyearsago

print(f"getting historic data from: {start_date}, to: {today}")

t_list = list_utils.get_nasdaq100() + list_utils.get_adhoc() + list_utils.get_snp500() + list_utils.get_aero_def()
t_list = list(set(t_list))

start_time = timing_utils.start(t_list)

filenames = file_utils.get_datasets_list()
t_list = list(set(t_list) - set(filenames))

if len(t_list) > 0:
    data = yf.download(t_list, start=start_date, end=today)

for symbol in t_list:
    try:
        tdata = pd.DataFrame()
        tdata = data.loc[:,(slice(None),symbol)]
        tdata.columns = COLUMNS
        if tdata['Close'].iloc[-1]:
            file_utils.save_historic_data(tdata, symbol)
    except Exception as e:
        continue

timing_utils.end(start_time)
    