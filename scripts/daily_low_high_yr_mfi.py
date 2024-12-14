import time,math,os
from datetime import date
import pandas as pd
pd.options.display.max_rows = 100000

start_time = time.time()

from yfinance_utils import mfi_utils

MIN_PRICE = 10.00
MIN_VOLUME = 1000000
COLUMNS = ["TICK", 'PRICE', 'MFI', 'MFI_AVERAGE', 'VOLUME']

FILE_NAME_MIN = f"out/{str(date.today())}_daily_lowest_yr_mfi.csv"
FILE_NAME_MAX = f"out/{str(date.today())}_daily_highest_yr_mfi.csv"

dfmfimin = pd.DataFrame(columns=COLUMNS)
dfmfimax = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')


print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")
rem = []

for tick in filenames:
    try:
        data = pd.read_csv(f"datasets/{tick}")
        if data['Close'].iloc[-1] < MIN_PRICE or data['Volume'].iloc[-1] < MIN_VOLUME:
            continue
        df_mfi = mfi_utils.get_mfi(data)

        mfi = df_mfi['mfi'].iloc[-1]
        mfimin = df_mfi['mfi'].min()
        mfimax = df_mfi['mfi'].max()
        mfiavg = df_mfi['mfi'].mean()
        price = df_mfi['Close'].iloc[-1]
        vol = df_mfi['Volume'].iloc[-1]

    except Exception as e:
        rem.append(tick)
        continue
    
    tmpmfi =  pd.DataFrame([[tick, price, mfi, mfiavg, vol]], columns=COLUMNS)

    if math.isclose(mfi,mfimin, abs_tol=2):
        dfmfimin = pd.concat([dfmfimin, tmpmfi], ignore_index=True)

    elif math.isclose(mfi,mfimax, abs_tol=2):
        dfmfimax = pd.concat([dfmfimax, tmpmfi], ignore_index=True)

    else:
        continue
        
print("CREATING FILE")
dfmfimin.round(2).to_csv(FILE_NAME_MIN, columns=COLUMNS)
dfmfimax.round(2).to_csv(FILE_NAME_MAX, columns=COLUMNS)
print(rem)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")