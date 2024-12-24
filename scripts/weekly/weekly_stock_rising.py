import os
import pandas as pd
from yfinance_utils import constants, timing_utils, file_utils

FILENAME = 'weekly_price_rising'
filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

df = pd.DataFrame()
ticker_list = []
weeks_list = []

for tick in filenames:
    data = file_utils.read_historic_data(tick)
    close = list(data['Close'])

    for i in range(5, len(close), 5):
        if close[i-5] > close[i]:
            continue
        else:
            if (i/5) > constants.WEEKS_RISING_MIN:
                ticker_list.append(tick)
                weeks_list.append(i/5)
            break

df["TICK"] = ticker_list
df["WEEKS"] = weeks_list

file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time)

