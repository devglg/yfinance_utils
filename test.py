
import yfinance
from yfinance_utils import rsi_utils

tick = yfinance.Ticker("AMD")
tick = rsi_utils.get_rsi(tick)
print(tick)



