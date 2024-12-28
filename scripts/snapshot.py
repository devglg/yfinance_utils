import pandas as pd
from datetime import date, timedelta
import yfinance as yf
from yfinance_utils import list_utils, timing_utils, file_utils, log_utils, constants

COLUMNS = ['Adj Close','Close','High','Low','Open','Volume']

twoyearsago = str(date.today() - timedelta(weeks=104))
oneyearago = str(date.today() - timedelta(weeks=52))
today=str(date.today())
tomorrow=str(date.today() + timedelta(days=1))

start_date = twoyearsago
end_date = tomorrow

t_list = list_utils.get_nasdaq100() + list_utils.get_adhoc() + list_utils.get_snp500() + list_utils.get_aero_def()
t_list = list(set(t_list))

start_time = timing_utils.start(t_list, 'snapshot', f'getting historic data from: {start_date} to: {end_date}')

data = yf.download(t_list, start=start_date, end=end_date, rounding=True)
for symbol in t_list:
    try:
        tdata = pd.DataFrame()
        tdata = data.loc[:,(slice(None),symbol)]
        tdata.columns = COLUMNS
        if tdata['Close'].iloc[-1] > constants.MINIMUM_PRICE:
            file_utils.save_historic_data(tdata, symbol)
    except Exception as e:
        continue

timing_utils.end(start_time, 'snapshot', f'data downloaded and saved')
    