import os
import pandas as pd
from datetime import date
from yfinance_utils import constants

def save_output_file(df, name):
    folder_path = f"{constants.OUTPUT_FOLDER}/{str(date.today())}"
    try:
        os.mkdir(folder_path)
    except Exception as e:
        pass

    name = f"{constants.OUTPUT_FOLDER}/{str(date.today())}/{name}.csv"
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
    try:
        os.mkdir(constants.DATA_FOLDER)
    except Exception as e:
        pass
    return df.to_csv(name)


def get_scripts_folder(t):
    if t == 'weekly':
        return constants.SCRIPTS_FOLDER_WEEKLY
    else:
        return constants.SCRIPTS_FOLDER_DAILY
    
def get_datasets_list():
    return os.listdir(constants.DATA_FOLDER)