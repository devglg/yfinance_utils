import math
import pandas as pd
from yfinance_utils import file_utils, timing_utils, signals_utils

COLUMNS = ["DATE", "TICK", 'PRICE', 'VOL', 'VOL AVG']
FILENAME_UP = 'daily_EMA_STOCH_MACD_UP'
FILENAME_DOWN = 'daily_EMA_STOCH_MACD_DOWN'

df = pd.DataFrame(columns=COLUMNS)
dfdown = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if math.isnan(data['Close'].iloc[-1]): continue
        vol_avg = data['Volume'].mean()

        if signals_utils.is_upward_trend(data) and \
                signals_utils.is_macd_cross_up(data, days_back=3, line=0) and \
                signals_utils.is_stoch_cross_up(data, days_back=3, line=20):

            tmp =  pd.DataFrame([[data['Date'].iloc[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1],
                                  vol_avg]], columns=COLUMNS)
            df = pd.concat([df, tmp], ignore_index=True)

        elif signals_utils.is_downward_trend(data) and \
                signals_utils.is_macd_cross_down(data, days_back=3, line=0) and \
                signals_utils.is_stoch_cross_down(data, days_back=3, line=80):

            tmp =  pd.DataFrame([[data['Date'].iloc[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1],
                                  vol_avg]], columns=COLUMNS)
            dfdown = pd.concat([dfdown, tmp], ignore_index=True)

        else:
            pass

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME_UP)
file_utils.save_output_file(dfdown,FILENAME_DOWN)
timing_utils.end(start_time)
