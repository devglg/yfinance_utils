import math, os
import pandas as pd
from yfinance_utils import mfi_utils, file_utils, constants, timing_utils

COLUMNS = ["TICK", 'PRICE', 'MFI', 'MFI_AVERAGE', 'VOLUME']

FILE_NAME_MIN = "daily_lowest_yr_mfi"
FILE_NAME_MAX = "daily_highest_yr_mfi"

dfmfimin = pd.DataFrame(columns=COLUMNS)
dfmfimax = pd.DataFrame(columns=COLUMNS)

filenames = os.listdir('datasets')

start_time = timing_utils.start(filenames)

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if data['Close'].iloc[-1] < constants.MINIMUM_PRICE or data['Volume'].iloc[-1] < constants.MINIMUM_VOLUME:
            continue
        df_mfi = mfi_utils.get_mfi(data)

        mfi = df_mfi['mfi'].iloc[-1]
        mfimin = df_mfi['mfi'].min()
        mfimax = df_mfi['mfi'].max()
        mfiavg = df_mfi['mfi'].mean()
        price = df_mfi['Close'].iloc[-1]
        vol = df_mfi['Volume'].iloc[-1]

    except Exception as e:
        continue
    
    tmpmfi =  pd.DataFrame([[tick, price, mfi, mfiavg, vol]], columns=COLUMNS)

    if math.isclose(mfi,mfimin, abs_tol=2):
        dfmfimin = pd.concat([dfmfimin, tmpmfi], ignore_index=True)

    elif math.isclose(mfi,mfimax, abs_tol=2):
        dfmfimax = pd.concat([dfmfimax, tmpmfi], ignore_index=True)

    else:
        continue
        
file_utils.save_output_file(dfmfimin, FILE_NAME_MIN)
file_utils.save_output_file(dfmfimax, FILE_NAME_MAX)
timing_utils.end(start_time)
