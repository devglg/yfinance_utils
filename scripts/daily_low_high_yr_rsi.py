import time,math,os
from datetime import date
import pandas as pd
pd.options.display.max_rows = 100000

start_time = time.time()

from yfinance import Tickers
from yfinance_utils import list_utils
from yfinance_utils import rsi_utils

COLUMNS = ["TICK", 'PRICE', 'RSI', 'RSI_AVERAGE', 'VOLUME']

FILE_NAME_MIN = f"out/{str(date.today())}_daily_lowest_yr_rsi.csv"
FILE_NAME_MAX = f"out/{str(date.today())}_daily_highest_yr_rsi.csv"

dfrsimin = pd.DataFrame(columns=COLUMNS)
dfrsimax = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')


print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")
rem = []

for tick in filenames:
    try:
        data = pd.read_csv(f"datasets/{tick}")

        df_rsi = rsi_utils.get_rsi(data)

        rsi = df_rsi['rsi'].iloc[-1]
        rsimin = df_rsi['rsi'].min()
        rsimax = df_rsi['rsi'].max()
        rsiavg = df_rsi['rsi'].mean()
        price = df_rsi['Close'].iloc[-1]
        vol = df_rsi['Volume'].iloc[-1]

    except Exception as e:
        rem.append(tick)
        continue
    
    tmprsi =  pd.DataFrame([[tick, price, rsi, rsiavg, vol]], columns=COLUMNS)
    if math.isclose(rsi,rsimin, abs_tol=2):
        dfrsimin = pd.concat([dfrsimin, tmprsi], ignore_index=True)
    elif math.isclose(rsi,rsimax, abs_tol=2):
        dfrsimax = pd.concat([dfrsimax, tmprsi], ignore_index=True)
    else:
        continue
        
print("CREATING FILE")
dfrsimin.round(2).to_csv(FILE_NAME_MIN, columns=COLUMNS)
dfrsimax.round(2).to_csv(FILE_NAME_MAX, columns=COLUMNS)
print(rem)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")