import os
import time
from datetime import date, timedelta
import yfinance as yf
from yfinance_utils import list_utils

COLUMNS = ['Adj Close','Close','High','Low','Open','Volume']
MIN_PRICE = 5.00

today=str(date.today())
print(f"today: {today}")
oneyearago = str(date.today() - timedelta(days=365))
print(f"one year ago: {oneyearago}")

t_list = list_utils.get_nasdaq100() + list_utils.get_adhoc() + list_utils.get_snp500() + list_utils.get_aero_def()
t_list = list(set(t_list))

print(f"getting {len(t_list)} tickers")

filenames = os.listdir('datasets')
failed = []
t_list = list(set(t_list + filenames))

for symbol in t_list:
    try:
        time.sleep(.5)
        if symbol in filenames: continue
        data = yf.download(symbol, start=oneyearago, end=today)
        # data = yf.download(symbol) # downloads all history
        data.columns = COLUMNS
        
        if data.empty: continue  # remove empty
        if data['Close'].iloc[-1] < MIN_PRICE: continue  # remove penny stocks

        data.to_csv(f"datasets/{symbol}", mode='w')
    except Exception as e:
        failed.append(symbol)

print("Failed:------")
print(failed)
    