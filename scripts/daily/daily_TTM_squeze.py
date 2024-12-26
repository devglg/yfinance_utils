import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from finta import TA
from yfinance_utils import file_utils, constants, timing_utils

FILENAME_UP = 'daily_TTM_squeeze_up'
FILENAME_DOWN = 'daily_TTM_squeeze_down'

COLUMNS=['DATE', 'TICK', 'PRICE', 'VOLUME', 'VOLUME pct of AVG', 'BB -3', 'KC -3', 'BB -1', 'KC -1']

df_up = pd.DataFrame(columns=COLUMNS)
df_down = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE: continue

        vol_avg = data['Volume'].iloc[-1] / data['Volume'].mean() * 100
        bb = TA.BBANDS(data)
        kc = TA.KC(data, kc_mult=1.5)
        if bb['BB_UPPER'].iloc[-3] < kc['KC_UPPER'].iloc[-3] and \
            bb['BB_UPPER'].iloc[-1] > kc['KC_UPPER'].iloc[-1] and \
            data['Close'].iloc[-1] > bb['BB_UPPER'].iloc[-1]:
            print(f"{tick:6}<<<----- HIGH ")     

            tmp = pd.DataFrame([[data['Date'].iloc[-1], tick, data['Close'].iloc[-1], data['Volume'].iloc[-1], vol_avg, bb['BB_UPPER'].iloc[-3], kc['KC_UPPER'].iloc[-3], bb['BB_UPPER'].iloc[-1], kc['KC_UPPER'].iloc[-1] ]], columns=COLUMNS)  
            df_up = pd.concat([df_up,tmp], ignore_index=True)

        if bb['BB_LOWER'].iloc[-3] > kc['KC_LOWER'].iloc[-3] and \
            bb['BB_LOWER'].iloc[-1] < kc['KC_LOWER'].iloc[-1] and \
            data['Close'].iloc[-1] < bb['BB_LOWER'].iloc[-1]:
            print(f"{tick:6}<<<----- LOW ")     

            tmp = pd.DataFrame([[data['Date'].iloc[-1], tick, data['Close'].iloc[-1], data['Volume'].iloc[-1], vol_avg, bb['BB_LOWER'].iloc[-3], kc['KC_LOWER'].iloc[-3], bb['BB_LOWER'].iloc[-1], kc['KC_LOWER'].iloc[-1] ]], columns=COLUMNS)  
            df_down = pd.concat([df_down,tmp], ignore_index=True)
        
    except Exception as e:
        pass

file_utils.save_output_file(df_up,FILENAME_UP)
file_utils.save_output_file(df_down,FILENAME_DOWN)
timing_utils.end(start_time)
