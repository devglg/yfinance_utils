import os
import pandas as pd
from yfinance import Tickers
from yfinance_utils import financials_utils, file_utils, timing_utils

COLUMNS = ["TICK", 'UP', 'GOOD', 'NEUTRAL', 'BAD', 'DOWN', 'TOTAL', 'AVERAGE UP']
FILENAME='weekly_upgrades'

dfups = pd.DataFrame(columns=COLUMNS)
filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

t = Tickers(filenames)

for tick in filenames:
    try:
        tmp = financials_utils.get_ratings(t.tickers[tick])

        up = tmp['up']
        good = tmp['Buy'] + tmp['Outperform'] + tmp['Overweight'] 
        down = tmp['down']
        bad = tmp['Underweight'] + tmp['Underperform'] 
        neutral = tmp['Hold'] + tmp['Neutral'] + tmp['Equal-Weight'] + tmp['Sector Weight']

        total = tmp['total']
        avg_good = ((good) / total) * 100

    except Exception as e:
        continue
    
    if up > down and good > bad:
        tmpups =  pd.DataFrame([[tick, up, good, neutral, bad, down, total, avg_good]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)

file_utils.save_output_file(dfups,FILENAME)
timing_utils.end(start_time)