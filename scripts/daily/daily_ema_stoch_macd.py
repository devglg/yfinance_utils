import os
import pandas as pd
from yfinance_utils import file_utils, timing_utils, signals_utils

COLUMNS = ["DATE", "TICK", 'PRICE', 'VOL', 'VOL AVG']
FILENAME = 'daily_EMA_STOCH_MACD'

df = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        vol_avg = data['Volume'].mean()

        if signals_utils.is_upward_trend(data) and \
                signals_utils.is_stoch_cross_up(data) and \
                signals_utils.is_macd_cross_up(data):
            
            tmp =  pd.DataFrame([[data['Date'].iloc[-1], 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  data['Volume'].iloc[-1],
                                  vol_avg]], columns=COLUMNS)
    
            df = pd.concat([df, tmp], ignore_index=True)

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time)
