import time, os, requests_cache
from datetime import date
import pandas as pd
from yfinance import Ticker, Tickers
from yfinance_utils import financials_utils

requests_cache.install_cache('api_cache')
pd.options.display.max_rows = 100000

COLUMNS = ["TICK", 'UP', 'GOOD', 'NEUTRAL', 'BAD', 'DOWN', 'TOTAL', 'AVERAGE UP']
FILENAME=f'out/{str(date.today())}_weekly_upgrades.csv'

dfups = pd.DataFrame(columns=COLUMNS)
filenames = os.listdir('datasets')

t = Tickers(filenames)

print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")

start_time = time.time()
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
        print(e, type(e))
        continue
    
    if up > down and good > bad:
        tmpups =  pd.DataFrame([[tick, up, good, neutral, bad, down, total, avg_good]], columns=COLUMNS)
        dfups = pd.concat([dfups, tmpups], ignore_index=True)

print("CREATING FILE")
dfups.round(0).to_csv(FILENAME, columns=COLUMNS)


print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")
