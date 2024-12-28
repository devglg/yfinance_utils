import os
import subprocess
import datetime
from yfinance_utils import file_utils, timing_utils, log_utils

today = datetime.date.today()
start_time = timing_utils.start([], 'run', f'{today.strftime("%A")} run: *** *** *** *** *** *** *** *** *** *** ***')
script_folders = []

subprocess.call([f'./.venv/bin/python3', f'./scripts/snapshot.py'])

script_folders.append(file_utils.get_scripts_folder('daily'))
if today.strftime('%A') in ['Saturday', 'Sunday']:
    script_folders.append(file_utils.get_scripts_folder('weekly'))

for folder in script_folders:
    filenames = os.listdir(folder)
    for file in filenames:
        print(f'Running script: {file}')
        subprocess.call([f'./.venv/bin/python3', f'./{folder}/{file}'])

timing_utils.end(start_time, 'run', f'completed, {today.strftime("%A")} run: ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^ ^^^')