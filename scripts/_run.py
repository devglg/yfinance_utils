import subprocess
import os
import datetime
from yfinance_utils import constants, file_utils

dirname = os.path.dirname(__file__)
output = os.listdir(constants.OUTPUT_FOLDER)

today = datetime.date.today()

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

if today.strftime('%A') in ['Saturday', 'Sunday']:
    filenames = os.listdir(file_utils.get_scripts_folder('weekly'))
    print('')
    print('***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***')
    print('')
    for f in filenames:
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./{file_utils.get_scripts_folder('weekly')}/{f}"])

else:
    filenames = os.listdir(file_utils.get_scripts_folder('daily'))
    print('')
    print('***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***')
    print('')
    for f in filenames:
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./{file_utils.get_scripts_folder('daily')}/{f}"])

