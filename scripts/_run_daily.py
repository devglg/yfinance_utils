import subprocess
import os

dirname = os.path.dirname(__file__)
filenames = os.listdir("scripts")

for f in filenames:
    if f.startswith('daily'):
        subprocess.call(["/Users/glg1/Documents/GitHub/yfinance_utils/.venv/bin/python3", f"scripts/{f}"])