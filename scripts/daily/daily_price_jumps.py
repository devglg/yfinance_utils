import os, datetime
import pandas as pd
from yfinance_utils import file_utils, constants, timing_utils

COLUMNS = ["DATE", "TICK", 'CLOSE', '% PRICE JUMP', 'VOLUME', '% VOLUME -1', '% VOLUME -2']

FILENAME_UP = 'daily_price_jump_up'
FILENAME_DOWN = 'daily_price_jump_down'

dfjumpup = pd.DataFrame(columns=COLUMNS)
dfjumpdown = pd.DataFrame(columns=COLUMNS)
filenames = file_utils.get_datasets_list()

start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        pctjump = (data["Close"].iloc[-1] - data["Close"].iloc[-2]) / data["Close"].iloc[-2] * 100
        
        if pctjump < constants.PERCENTAGE_MOVE and pctjump > -(constants.PERCENTAGE_MOVE): continue
        
        pctvol = (data["Volume"].iloc[-1] - data["Volume"].iloc[-2]) / data["Volume"].iloc[-2] * 100
        pctvol2 = (data["Volume"].iloc[-2] - data["Volume"].iloc[-3]) / data["Volume"].iloc[-3] * 100
    except Exception as e:
        continue
    
    tmpjump =  pd.DataFrame([[data['Date'].iloc[-1], tick, data['Close'].iloc[-1], pctjump, data['Volume'].iloc[-1], pctvol, pctvol2]], columns=COLUMNS)
    if pctjump > 0:
        dfjumpup = pd.concat([dfjumpup, tmpjump], ignore_index=True)
    else:
        dfjumpdown = pd.concat([dfjumpdown, tmpjump], ignore_index=True)

file_utils.save_output_file(dfjumpup,FILENAME_UP)
file_utils.save_output_file(dfjumpdown,FILENAME_DOWN)
timing_utils.end(start_time)
