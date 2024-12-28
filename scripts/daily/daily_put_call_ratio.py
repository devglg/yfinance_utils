import pandas as pd
import math
import yfinance
from yfinance_utils import file_utils, timing_utils, ratio_utils, options_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'VOLUME', 'CALLS', 'PUTS', 'C/P RATIO', 'SENTIMENT']
FILENAME = 'daily_put_call_ratio'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, f'{FILENAME}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        t = yfinance.Ticker(tick)

        calls = options_utils.get_calls_volume(t)
        puts = options_utils.get_puts_volume(t)
        pcr = ratio_utils.get_put_call_ratio(t)

        if math.isnan(calls) or math.isnan(puts) or math.isnan(pcr): continue
        sentiment = ''

        if pcr > 0.7:
            sentiment = 'bearish'
        else:
            sentiment = 'bullish'

        tmp =  pd.DataFrame([[data.index[-1], 
                                tick, 
                                data['Close'].iloc[-1],
                                data['Volume'].iloc[-1],
                                calls,
                                puts,
                                pcr,
                                sentiment
                                ]], columns=COLUMNS)

        df = pd.concat([df, tmp], ignore_index=True)
    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, f'{FILENAME}')
