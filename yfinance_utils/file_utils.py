import pandas as pd
from datetime import date
from yfinance_utils import constants

def save_output_file(df, name):
    name = f"out/{str(date.today())}_{name}.csv"
    ticks = df['TICK']
    url = []
    for i in ticks:
        url.append(f"{constants.QUOTE_BASE_URL}/{i}/")
    df['URL'] = url
    df.round(2).to_csv(name, index=False)

def read_historic_data(name):
    name = f"{constants.DATA_FOLDER}/{name}"
    return pd.read_csv(name)

def save_historic_data(df, name):
    name = f'{constants.DATA_FOLDER}/{name}'
    return df.to_csv(name)