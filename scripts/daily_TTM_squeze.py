import warnings
warnings.filterwarnings("ignore")

import time, os, yfinance, config
from datetime import date
import pandas as pd
from finta import TA

FILENAME=f'{str(date.today())}_daily_TTM_squeeze'
COLUMNS=['TICK', 'PRICE', 'VOLUME', 'VOLUME pct of AVG', 'BB -3', 'KC -3', 'BB -1', 'KC -1']
df_up = pd.DataFrame(columns=COLUMNS)
df_down = pd.DataFrame(columns=COLUMNS)

c = config.get_constants()


filenames = os.listdir('datasets')
print(f"scrubbing {len(filenames)} companies.")
print("-------------------------------------------------------------------------------------------------")

start_time = time.time()
for tick in filenames:
    try:
        data = pd.read_csv(f"datasets/{tick}")
        vol_avg = data['Volume'].iloc[-1] / data['Volume'].mean() * 100
        bb = TA.BBANDS(data)
        kc = TA.KC(data, kc_mult=1.5)
        if bb['BB_UPPER'].iloc[-3] < kc['KC_UPPER'].iloc[-3] and \
            bb['BB_UPPER'].iloc[-1]>kc['KC_UPPER'].iloc[-1] and \
            data['Close'].iloc[-1] > bb['BB_UPPER'].iloc[-1] and \
            data['Close'].iloc[-1] > c.MINIMUM_PRICE:
            print(tick,"<<<---------------------- HIGH ")     

            tmp = pd.DataFrame([[tick, data['Close'].iloc[-1], data['Volume'].iloc[-1], vol_avg, bb['BB_UPPER'].iloc[-3], kc['KC_UPPER'].iloc[-3], bb['BB_UPPER'].iloc[-1], kc['KC_UPPER'].iloc[-1] ]], columns=COLUMNS)  
            df_up = pd.concat([df_up,tmp], ignore_index=True)

        if bb['BB_LOWER'].iloc[-3] > kc['KC_LOWER'].iloc[-3] and \
            bb['BB_LOWER'].iloc[-1] < kc['KC_LOWER'].iloc[-1] and \
            data['Close'].iloc[-1] < bb['BB_LOWER'].iloc[-1] and \
            data['Close'].iloc[-1] > c.MINIMUM_PRICE:
            print(tick,"<<<---------------------- LOW ")     

            tmp = pd.DataFrame([[tick, data['Close'].iloc[-1], data['Close'].iloc[-1], vol_avg, bb['BB_LOWER'].iloc[-3], kc['KC_LOWER'].iloc[-3], bb['BB_LOWER'].iloc[-1], kc['KC_LOWER'].iloc[-1] ]], columns=COLUMNS)  
            df_down = pd.concat([df_down,tmp], ignore_index=True)
        
    except Exception as e:
        pass

df_up.round(2).to_csv(f"out/{FILENAME}_up.csv", index=False)
df_down.round(2).to_csv(f"out/{FILENAME}_down.csv", index=False)

print("TIMING")
end_time = time.time()
print(f"time: {(end_time - start_time)/60} minutes")