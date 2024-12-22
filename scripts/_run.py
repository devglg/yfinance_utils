import subprocess
import os, sys
import datetime
from yfinance_utils import constants

dirname = os.path.dirname(__file__)
filenames = os.listdir(constants.SCRIPTS_FOLDER)
output = os.listdir(constants.OUTPUT_FOLDER)

today = datetime.date.today()

if today.strftime('%A') in ['Saturday', 'Sunday']:
    print('')
    print('***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***  WEEKLY  ***')
    print('')
else:
    print('')
    print('***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***  DAILY  ***')
    print('')

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

for f in filenames:
    if today.strftime('%A') in ['Saturday', 'Sunday']:
        if f.startswith('weekly'):
            print(f'Running script: {f}')
            subprocess.call([f"./.venv/bin/python3", f"./{constants.SCRIPTS_FOLDER_WEEKLY}/{f}"])
    else:
        if f.startswith('daily'):
            print(f'Running script: {f}')
            subprocess.call([f"./.venv/bin/python3", f"./{constants.SCRIPTS_FOLDER_DAILY}/{f}"])