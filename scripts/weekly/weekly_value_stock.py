import pandas as pd
import yfinance, math
from yfinance_utils import file_utils, timing_utils, constants, ratio_utils

COLUMNS = ['DATE', 'TICK', 'PRICE', 'PRICE_TO_EARNINGS', 'PRICE_TO_SALES']
FILENAME = 'daily_value_stock'

df = pd.DataFrame(columns=COLUMNS)

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, f'{FILENAME}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        t = yfinance.Ticker(tick)
        last_price = data['Close'].iloc[-1]

        price_to_earnings = ratio_utils.get_price_to_earnings(t)
        if math.isnan(price_to_earnings) or price_to_earnings > constants.MAXIMUM_PRICE_TO_EARNINGS or price_to_earnings < 0.00:
            continue

        price_to_sales = ratio_utils.get_price_to_sales(t)
        if math.isnan(price_to_sales) or price_to_sales < constants.MAXIMUM_PRICE_TO_SALES:
            continue

        tmp = pd.DataFrame([[data.index[-1],tick, last_price, price_to_earnings, price_to_sales]], columns=df.columns)
        df = pd.concat([tmp, df], ignore_index=True)
    except Exception as e:
        continue
    
file_utils.save_output_file(df,FILENAME)
timing_utils.end(start_time, FILENAME)
