import subprocess
import os

dirname = os.path.dirname(__file__)
filenames = os.listdir("scripts")

subprocess.call([f"./.venv/bin/python3", f"./scripts/snapshot.py"])

for f in filenames:
    if f.startswith('daily'):
        print(f'Running script: {f}')
        subprocess.call([f"./.venv/bin/python3", f"./scripts/{f}"])