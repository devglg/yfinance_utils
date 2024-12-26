import math, os, datetime
import pandas as pd
from yfinance_utils import rsi_utils, file_utils, timing_utils

COLUMNS = ["DATE", "TICK", 'PRICE', 'RSI', 'RSI_AVERAGE', 'VOLUME']

FILE_NAME_MIN = "daily_rsi_year_lowest"
FILE_NAME_MAX = "daily_rsi_year_highest"

dfrsimin = pd.DataFrame(columns=COLUMNS)
dfrsimax = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')
start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        df_rsi = rsi_utils.get_rsi(data)

        rsi = df_rsi['rsi'].iloc[-1]
        rsimin = df_rsi['rsi'].min()
        rsimax = df_rsi['rsi'].max()
        rsiavg = df_rsi['rsi'].mean()
        price = df_rsi['Close'].iloc[-1]
        vol = df_rsi['Volume'].iloc[-1]

    except Exception as e:
        continue
    
    tmprsi =  pd.DataFrame([[data['Date'].iloc[-1], tick, price, rsi, rsiavg, vol]], columns=COLUMNS)
    if math.isclose(rsi,rsimin, abs_tol=2):
        dfrsimin = pd.concat([dfrsimin, tmprsi], ignore_index=True)
    elif math.isclose(rsi,rsimax, abs_tol=2):
        dfrsimax = pd.concat([dfrsimax, tmprsi], ignore_index=True)
    else:
        continue
        
file_utils.save_output_file(dfrsimin,FILE_NAME_MIN)
file_utils.save_output_file(dfrsimax,FILE_NAME_MAX)
timing_utils.end(start_time)
