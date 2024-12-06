import time
from datetime import date
import pandas as pd
pd.options.display.max_rows = 100000

start_time = time.time()

import statistics
from yfinance import Tickers
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils
from yfinance_utils import financials_utils

COLUMNS = ["TICK", 'RSI', 'PRICE', 'UP', 'NEUTRAL', 'DOWN', 'TOTAL', 'AVERAGE UP']

FILE_NAME = "upgrades_up"

dfups = pd.DataFrame(columns=COLUMNS)

t_list = list_utils.get_nasdaq() + list_utils.get_rus2000() + list_utils.get_snp500()
t_list = list(set(t_list))

print(f"scrubbing {len(t_list)} companies.")
print("-------------------------------------------------------------------------------------------------")
ts = Tickers(t_list)
rem = []

for tick in ts.tickers:
    try:
        t = ts.tickers[tick]
        df_rsi = rsi_utils.get_rsi(t)
        tmp = financials_utils.get_ratings(t)

        rsi = df_rsi['rsi'].iloc[-1]
        price = df_rsi['Close'].iloc[-1]

        up = tmp['up'] + tmp['Buy'] + tmp['Outperform'] + tmp['Overweight'] 
        down = tmp['down'] + tmp['Underweight'] + tmp['Underperform'] 
        neutral = tmp['Hold'] + tmp['Neutral'] + tmp['Equal-Weight'] + tmp['Sector Weight']

        total = tmp['total']
        avg = up / total * 100

    except Exception as e:
        rem.append(tick)
        continue
    
    if tmp['up'] > tmp['down']:
        tmpups =  pd.DataFrame([[tick, rsi, price, up, neutral, down, total, avg]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)

print("CREATING FILE")
dfups.round(0).to_csv(f'{str(date.today())}_{FILE_NAME}.csv', columns=COLUMNS)
print(rem)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")