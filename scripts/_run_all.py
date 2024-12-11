import subprocess

# subprocess.call(["/Users/glg-1/Documents/GitHub/yfinance_utils/.venv/bin/python3", "/Users/glg-1/Documents/GitHub/yfinance_utils/scripts/snapshots_clean.py"])
subprocess.call(["/Users/glg-1/Documents/GitHub/yfinance_utils/.venv/bin/python3", "/Users/glg-1/Documents/GitHub/yfinance_utils/scripts/snapshot.py"])
subprocess.call(["/Users/glg-1/Documents/GitHub/yfinance_utils/.venv/bin/python3", "/Users/glg-1/Documents/GitHub/yfinance_utils/scripts/daily_TTM_squeze.py"])
subprocess.call(["/Users/glg-1/Documents/GitHub/yfinance_utils/.venv/bin/python3", "/Users/glg-1/Documents/GitHub/yfinance_utils/scripts/daily_volume.py"])
subprocess.call(["/Users/glg-1/Documents/GitHub/yfinance_utils/.venv/bin/python3", "/Users/glg-1/Documents/GitHub/yfinance_utils/scripts/daily_price_jumps.py"])
