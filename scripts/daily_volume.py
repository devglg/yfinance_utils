import time, os
from datetime import date

start_time = time.time()
import pandas as pd
import statistics

from yfinance_utils import rsi_utils

COLUMNS = ["TICK", 'RSI', 'AVERAGE', 'PRICE -1', 'VOLUME -1', 'VOL % -1', 'PRICE', 'VOLUME', 'VOL %']

MINIMUM_RSI = 50.0
MINIMUM_PRICE = 10.0
MINIMUM_VOLUME = 1000000

FILENAME=f'out/{str(date.today())}_daily_volume_up.csv'

dfvol = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')

print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")
rem = []

for tick in filenames:
    try:
        data = pd.read_csv(f"datasets/{tick}")
        if data["Close"].iloc[-1] <  MINIMUM_PRICE:
            continue

        if data["Volume"].iloc[-1] < MINIMUM_VOLUME:
            continue

        d_rsi = rsi_utils.get_rsi(data, window_length=14)
        if d_rsi["rsi"].iloc[-1] < MINIMUM_RSI:
            continue

        avg = int(statistics.mean(d_rsi["Volume"]))
        volume_0 = d_rsi["Volume"].iloc[-1]
        volume_0_pct = volume_0/avg*100
        volume_1 = d_rsi["Volume"].iloc[-2]
        volume_1_pct = volume_1/avg*100

        price_0 = d_rsi["Close"].iloc[-1]
        price_1 = d_rsi["Close"].iloc[-2]

        rsi = d_rsi["rsi"].iloc[-1]
        price = d_rsi["Close"].iloc[-1]
    except Exception as e:
        print(e)
        rem.append(tick)
        continue
    
    if volume_0_pct > 150 and volume_1_pct < 110:
        tmpvol =  pd.DataFrame([[tick, rsi, avg, price_1, volume_1, volume_1_pct, price_0, volume_0, volume_0_pct]], columns=COLUMNS)
        dfvol = pd.concat([dfvol, tmpvol], ignore_index=True)


print("CREATING FILE")
dfvol.round(0).to_csv(FILENAME, columns=COLUMNS)
print(rem)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")