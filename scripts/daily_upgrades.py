import os
import pandas as pd
from yfinance import Tickers
from yfinance_utils import financials_utils, file_utils, timing_utils, constants

COLUMNS = ["TICK", 'GOOD', 'BAD', 'NEUTRAL', 'TOTAL', 'AVG', 'UP/-DOWN']
FILE_NAME_UP = 'daily_upgrades_up'
FILE_NAME_DOWN = 'daily_upgrades_down'

dfups = pd.DataFrame(columns=COLUMNS)
dfdowns = pd.DataFrame(columns=COLUMNS)

t_list = os.listdir('datasets')
start_time = timing_utils.start(t_list)

ts = Tickers(t_list)

for tick in ts.tickers:
    try:
        t = ts.tickers[tick]
        data = file_utils.read_historic_data(tick)
        tmp = financials_utils.get_ratings(t)

        up = tmp['up']
        down = tmp['down'] 
        good = tmp['up'] + tmp['Buy'] + tmp['Outperform'] + tmp['Overweight'] 
        bad = tmp['down'] + tmp['Underweight'] + tmp['Underperform'] 
        neutral = tmp['Hold'] + tmp['Neutral'] + tmp['Equal-Weight'] + tmp['Sector Weight']

        total = good + bad + neutral
        avg = good / total * 100

    except Exception as e:
        continue
    
    if avg > constants.PERCENTAGE_GOOD_RATING:
        if up > down:
            tmp =  pd.DataFrame([[tick, good, bad, neutral, total, avg, up - down]], columns=COLUMNS)
            dfups = pd.concat([dfups, tmp], ignore_index=True)

        if up < down:
            tmp =  pd.DataFrame([[tick, good, bad, neutral, total, avg, up - down]], columns=COLUMNS)
            dfdowns = pd.concat([dfdowns, tmp], ignore_index=True)

file_utils.save_output_file(dfups,FILE_NAME_UP)
file_utils.save_output_file(dfdowns,FILE_NAME_DOWN)
timing_utils.end(start_time)
