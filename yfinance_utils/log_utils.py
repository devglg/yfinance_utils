import os
from datetime import datetime
from yfinance_utils import constants

def create_folder():
    try:
        os.mkdir(f'{constants.OUTPUT_FOLDER}/{constants.LOG_FOLDER}')
    except Exception as e:
        pass

def log(file, msg):
    create_folder()
    filename = f"{constants.OUTPUT_FOLDER}/{constants.LOG_FOLDER}/{constants.LOG_FILENAME}"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as f:
        f.write(f'{ts}, {file}, {msg}\n')
    f.close()
