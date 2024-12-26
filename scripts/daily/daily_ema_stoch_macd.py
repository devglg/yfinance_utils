import os, datetime
import pandas as pd
from finta import TA
from yfinance_utils import file_utils, timing_utils

COLUMNS = ["DATE", "TICK", 'PRICE', 'EMA200', 'EMA200 PCT', 'STOCHK', 'STOCHD', 'MACD', 'MACDS', 'VOL', 'VOL AVG']
FILENAME = 'daily_EMA_STOCH_MACD'

df = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        ema200 = TA.EMA(data, 200)
        ema200pct = data['Close'].iloc[-1] / ema200.iloc[-1] * 100
        stochk = TA.STOCH(data)
        stochd = TA.STOCHD(data)
        macd = TA.MACD(data)
        vol_avg = data['Volume'].mean()

        def macd_cross(data):
            return data['MACD'].iloc[-1] > macd['SIGNAL'].iloc[-1] and \
                   data['MACD'].iloc[-5] < macd['SIGNAL'].iloc[-5]
        
        def stoch_cross(k, d):
            return k.iloc[-1] > d.iloc[-1] and \
                   k.iloc[-5] < d.iloc[-5] and \
                   k.iloc[-1] > 20 and k.iloc[-5] < 20

        if data['Close'].iloc[-1] > ema200.iloc[-1] and \
                stoch_cross(stochk, stochd) and \
                macd_cross(macd):
            
            tmp =  pd.DataFrame([[datetime.date.today(), 
                                  tick, 
                                  data['Close'].iloc[-1],
                                  ema200.iloc[-1],
                                  ema200pct, 
                                  stochk.iloc[-1], 
                                  stochd.iloc[-1], 
                                  macd['MACD'].iloc[-1], 
                                  macd['SIGNAL'].iloc[-1], 
                                  data['Volume'].iloc[-1],
                                  vol_avg]], columns=COLUMNS)
    
            df = pd.concat([df, tmp], ignore_index=True)

    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time)
