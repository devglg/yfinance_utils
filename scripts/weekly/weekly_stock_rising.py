import os
import pandas as pd
from yfinance_utils import constants, timing_utils, file_utils

FILENAME = 'weekly_price_rising'
filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

df = pd.DataFrame()
ticker_list = []
weeks_list = []
rise_pct = []

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        close = list(data['Close'])

        counter = 0
        for i in range(len(close)-1, 10, -5):
            counter = counter + 1
            if close[i] > close[i-5]:
                continue
            else:
                if (counter) > constants.MINIMUM_WEEKS_RISING:
                    ticker_list.append(tick)
                    weeks_list.append(counter)
                    rise_pct.append((close[len(close)-1] / close[counter]) * 100)
                break
    except Exception as e:
        continue

df["TICK"] = ticker_list
df["WEEKS"] = weeks_list
df["RISE PCT"] = rise_pct

file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time)

