import subprocess
import os
import datetime
from yfinance_utils import constants, file_utils, timing_utils, log_utils

# dirname = os.path.dirname(__file__)
# output = os.listdir(constants.OUTPUT_FOLDER)
today = datetime.date.today()

start_time = timing_utils.start([])

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

if today.strftime('%A') in ['Saturday', 'Sunday']:
    filenames = os.listdir(file_utils.get_scripts_folder('weekly'))
    log_utils.log(f'Starting weekly run.')
    print('')
    print('***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***')
    print('')
    for f in filenames:
        log_utils.log(f'{f} script starting.')
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./{file_utils.get_scripts_folder('weekly')}/{f}"])
        log_utils.log(f'{f} script completed.')

else:
    filenames = os.listdir(file_utils.get_scripts_folder('daily'))
    log_utils.log(f'Starting daily run.')
    print('')
    print('***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***')
    print('')
    for f in filenames:
        log_utils.log(f'{f} script starting.')
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./{file_utils.get_scripts_folder('daily')}/{f}"])
        log_utils.log(f'{f} script completed.')

timing_utils.end(start_time)