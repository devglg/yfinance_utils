import os
import subprocess
import datetime
from yfinance_utils import file_utils, timing_utils, log_utils

today = datetime.date.today()
start_time = timing_utils.start([])
script_folder = ''

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

if today.strftime('%A') in ['Saturday', 'Sunday']:
    script_folder = file_utils.get_scripts_folder('weekly')
else:
    script_folder = file_utils.get_scripts_folder('daily')

log_utils.log(f'Starting run from {script_folder} *** *** *** *** *** *** *** *** *** *** ***')
filenames = os.listdir(script_folder)

for f in filenames:
    log_utils.log(f'{f} starting.')
    print(f'Running script: {f}')
    subprocess.call([f"./.venv/bin/python3", f"./{script_folder}/{f}"])
    log_utils.log(f'{f} completed.')

log_utils.log('END RUN ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^   ^^^')
timing_utils.end(start_time)