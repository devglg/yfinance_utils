import os
import pandas as pd
from yfinance_utils import rsi_utils, file_utils, constants, timing_utils

COLUMNS = ["TICK", 'CLOSE', 'PERCENTAGE JUMP', 'VOLUME', 'PERCENT_VOLUME -2', 'PERCENT_VOLUME-1', 'RSI-2', 'RSI-1']

FILENAME = 'daily_price_jump'

dfjump = pd.DataFrame(columns=COLUMNS)
filenames = os.listdir('datasets')

start_time = timing_utils.start(filenames)

jumps = []
for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if data["Close"].iloc[-1] < constants.MINIMUM_PRICE: continue
        if data["Volume"].iloc[-1] < constants.MINIMUM_VOLUME: continue
        pctjump = (data["Close"].iloc[-1] - data["Close"].iloc[-2]) / data["Close"].iloc[-2] * 100
        
        if pctjump < constants.PERCENTAGE_MOVE: continue
        
        rsi = rsi_utils.get_rsi(data)
        rsijump = rsi['rsi'].iloc[-2]
        rsijump2 = rsi['rsi'].iloc[-3]
        pctvol = (data["Volume"].iloc[-2] - data["Volume"].iloc[-3]) / data["Volume"].iloc[-3] * 100
        pctvol2 = (data["Volume"].iloc[-3] - data["Volume"].iloc[-4]) / data["Volume"].iloc[-4] * 100
        jumps.append(tick)
    except Exception as e:
        continue
    
    tmpjump =  pd.DataFrame([[tick, data['Close'].iloc[-1], pctjump, data['Volume'].iloc[-1], pctvol2, pctvol, rsijump2 ,rsijump]], columns=COLUMNS)
    dfjump = pd.concat([dfjump, tmpjump], ignore_index=True)

file_utils.save_output_file(dfjump,FILENAME)
timing_utils.end(start_time)
