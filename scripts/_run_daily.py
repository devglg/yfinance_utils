import subprocess
import os

dirname = os.path.dirname(__file__)
filenames = os.listdir("scripts")

for f in filenames:
    if f.startswith('daily'):
        print(f)
        subprocess.call([f"./.venv/bin/python3", f"./scripts/{f}"])