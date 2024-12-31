import pandas as pd
from yfinance_utils import file_utils, timing_utils

FILENAME = 'daily_volume_total'
dfvol = pd.DataFrame()

filenames = file_utils.get_datasets_list()
start_time = timing_utils.start(filenames, f'{FILENAME}')

for tick in filenames:
    try:
        data = file_utils.read_historic_data(tick)
        if not 'DATE' in dfvol.columns:
            dfvol['DATE'] = data.index

        dfvol[tick] = data['Volume']

    except Exception as e:
        continue

dfvol['TOTAL'] = dfvol.sum(axis=1)
file_utils.save_output_file(dfvol, FILENAME)
timing_utils.end(start_time, f'{FILENAME}')
