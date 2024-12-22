import subprocess
import os
import datetime

dirname = os.path.dirname(__file__)
filenames = os.listdir("scripts")
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
            subprocess.call([f"./.venv/bin/python3", f"./scripts/{f}"])
    else:
        if f.startswith('daily'):
            print(f'Running script: {f}')
            subprocess.call([f"./.venv/bin/python3", f"./scripts/{f}"])