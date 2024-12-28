import os
import subprocess
import datetime
from yfinance_utils import file_utils, timing_utils, log_utils

today = datetime.date.today()
start_time = timing_utils.start([], f'start {today.strftime("%A")} run: *** *** *** *** *** *** *** *** *** *** ***')
script_folders = []

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

script_folders.append(file_utils.get_scripts_folder('daily'))
if today.strftime('%A') in ['Saturday', 'Sunday']:
    script_folders.append(file_utils.get_scripts_folder('weekly'))

for folder in script_folders:
    filenames = os.listdir(folder)
    for f in filenames:
        log_utils.log(f'{f} starting.')
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./{folder}/{f}"])
        log_utils.log(f'{f} completed.')

timing_utils.end(start_time, f'complete {today.strftime("%A")} run: ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^')