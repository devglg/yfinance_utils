import pandas as pd
from yfinance_utils import file_utils, timing_utils, signals_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'VOLUME']
FILENAME_HIGH = 'daily_52_week_high'
FILENAME_LOW = 'daily_52_week_low'

dfhigh = pd.DataFrame(columns=COLUMNS)
dflow = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames,f'{FILENAME_HIGH}-{FILENAME_LOW}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if signals_utils.is_52wk_high(data):
            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1]
                                  ]], columns=COLUMNS)

            dfhigh = pd.concat([dfhigh, tmp], ignore_index=True)

        elif signals_utils.is_52wk_low(data):
            tmp =  pd.DataFrame([[data.index[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1]
                                  ]], columns=COLUMNS)

            dflow = pd.concat([dflow, tmp], ignore_index=True)
        else:
            pass

    except Exception as e:
        continue
    
file_utils.save_output_file(dfhigh,FILENAME_HIGH)
file_utils.save_output_file(dflow,FILENAME_LOW)
timing_utils.end(start_time, f'{FILENAME_HIGH}-{FILENAME_LOW}')
