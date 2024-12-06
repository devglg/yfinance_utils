import time, os
from datetime import date

start_time = time.time()
import pandas as pd
from yfinance_utils import rsi_utils

COLUMNS = ["TICK", 'CLOSE', 'PERCENTAGE JUMP', 'VOLUME', 'PERCENT_VOLUME -2', 'PERCENT_VOLUME-1', 'RSI-2', 'RSI-1']
PERCENTAGE_MOVE = 5.0
MINIMUM_PRICE = 10.0
MINIMUM_VOLUME = 1000000
FILENAME=f'out/{str(date.today())}_daily_price_jump.csv'

dfjump = pd.DataFrame(columns=COLUMNS)
filenames = os.listdir('datasets')

print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")
nodata = []
jumps = []
for tick in filenames:
    try:
        data = pd.read_csv(f"datasets/{tick}")
        if data["Close"].iloc[-1] < MINIMUM_PRICE: continue
        if data["Volume"].iloc[-1] < MINIMUM_VOLUME: continue
        pctjump = (data["Close"].iloc[-1] - data["Close"].iloc[-2]) / data["Close"].iloc[-2] * 100
        
        if pctjump <  PERCENTAGE_MOVE:continue
        
        rsi = rsi_utils.get_rsi(data)
        rsijump = rsi['rsi'].iloc[-2]
        rsijump2 = rsi['rsi'].iloc[-3]
        pctvol = (data["Volume"].iloc[-2] - data["Volume"].iloc[-3]) / data["Volume"].iloc[-3] * 100
        pctvol2 = (data["Volume"].iloc[-3] - data["Volume"].iloc[-4]) / data["Volume"].iloc[-4] * 100
        jumps.append(tick)
    except Exception as e:
        nodata.append(tick)
        continue
    tmpjump =  pd.DataFrame([[tick, data['Close'].iloc[-1], pctjump, data['Volume'].iloc[-1], pctvol2, pctvol, rsijump2 ,rsijump]], columns=COLUMNS)
    dfjump = pd.concat([dfjump, tmpjump], ignore_index=True)


print("CREATING FILE")
dfjump.round(0).to_csv(FILENAME, columns=COLUMNS)
print(nodata)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")