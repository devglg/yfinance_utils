import os
import pandas as pd
from yfinance import Tickers
from yfinance_utils import rsi_utils, financials_utils, file_utils, constants, timing_utils

COLUMNS = ["TICK", 'RSI', 'PRICE', 'UP', 'NEUTRAL', 'DOWN', 'TOTAL', 'AVERAGE UP']
FILE_NAME = 'daily_upgrades_up'

dfups = pd.DataFrame(columns=COLUMNS)

t_list = os.listdir('datasets')
start_time = timing_utils.start(t_list)

ts = Tickers(t_list)

for tick in ts.tickers:
    try:
        t = ts.tickers[tick]
        data = file_utils.read_historic_data(tick)
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE or data['Volume'].iloc[-1] < constants.MINIMUM_VOLUME:
            continue

        df_rsi = rsi_utils.get_rsi(data)
        tmp = financials_utils.get_ratings(t)

        rsi = df_rsi['rsi'].iloc[-1]
        price = df_rsi['Close'].iloc[-1]

        up = tmp['up'] + tmp['Buy'] + tmp['Outperform'] + tmp['Overweight'] 
        down = tmp['down'] + tmp['Underweight'] + tmp['Underperform'] 
        neutral = tmp['Hold'] + tmp['Neutral'] + tmp['Equal-Weight'] + tmp['Sector Weight']

        total = tmp['total']
        avg = up / total * 100

    except Exception as e:
        continue
    
    if tmp['up'] > tmp['down']:
        tmpups =  pd.DataFrame([[tick, rsi, price, up, neutral, down, total, avg]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)


file_utils.save_output_file(dfups,FILE_NAME)
timing_utils.end(start_time)
