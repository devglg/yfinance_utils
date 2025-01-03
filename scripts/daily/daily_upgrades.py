import datetime
import pandas as pd
from yfinance import Tickers
from yfinance_utils import financials_utils, file_utils, timing_utils

COLUMNS = ['DATE', 'TICK', 'UP', 'DOWN', 'HOLD', 'AVG', 'TOTAL']
FILENAME='daily_upgrades'

dfups = pd.DataFrame(columns=COLUMNS)
filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, FILENAME)

t = Tickers(filenames)

for tick in filenames:
    try:
        # TODO: change this to t.recommendstions
        tmp = financials_utils.get_ratings(t.tickers[tick])
        up = tmp['up']
        down = tmp['down']
        hold = tmp['hold']
        total = tmp['total']
        avg_up = ((up) / total) * 100

    except Exception as e:
        continue
    
    if up > down:
        tmpups =  pd.DataFrame([[datetime.date.today(), tick, up, down, hold, avg_up, total]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)

file_utils.save_output_file(dfups,FILENAME)
timing_utils.end(start_time, FILENAME)