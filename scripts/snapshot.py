import os
import time
from datetime import date, timedelta
import yfinance as yf
from yfinance_utils import list_utils, constants, timing_utils, file_utils

COLUMNS = ['Adj Close','Close','High','Low','Open','Volume']

today=str(date.today())
oneyearago = str(date.today() - timedelta(weeks=52))
twoyearsago = str(date.today() - timedelta(weeks=104))

print(f"getting historic data from: {oneyearago}, to: {today}")

t_list = list_utils.get_nasdaq100() + list_utils.get_adhoc() + list_utils.get_snp500() + list_utils.get_aero_def()
t_list = list(set(t_list))

start_time = timing_utils.start(t_list)

filenames = os.listdir(constants.DATA_FOLDER)
t_list = list(set(t_list) - set(filenames))

for symbol in t_list:
    try:
        data = yf.download(symbol, start=twoyearsago, end=today)
        # data = yf.download(symbol) # downloads all history
        data.columns = COLUMNS
        
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE: continue  # remove penny stocks
        file_utils.save_historic_data(data, symbol)
    except Exception as e:
        continue

timing_utils.end(start_time)
    