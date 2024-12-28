from finta import TA


def is_macd_cross_up(data, days_back = 5, line = 10):
    macd = TA.MACD(data)

    return macd['MACD'].iloc[-1] > macd['SIGNAL'].iloc[-1] \
           and macd['MACD'].iloc[-days_back] < macd['SIGNAL'].iloc[-days_back] \
           and macd['MACD'].iloc[-1] < line

def is_macd_cross_down(data, days_back = 5, line = -10):
    macd = TA.MACD(data)
    return macd['MACD'].iloc[-1] < macd['SIGNAL'].iloc[-1] \
           and macd['MACD'].iloc[-days_back] > macd['SIGNAL'].iloc[-days_back] \
           and macd['MACD'].iloc[-1] > line

def is_stoch_cross_up(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] > stochd.iloc[-1] \
           and stochk.iloc[-days_back] < stochd.iloc[-days_back] \
           and stochk.iloc[-1] > line and stochk.iloc[-days_back] < line

def is_stoch_cross_down(data, days_back = 5, line = 50):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] < stochd.iloc[-1] \
           and stochk.iloc[-days_back] > stochd.iloc[-days_back] \
           and stochk.iloc[-1] < line and stochk.iloc[-days_back] > line

def is_upward_trend(data):
    ema200 = TA.EMA(data, 200)
    return data['Close'].iloc[-1] > ema200.iloc[-1]

def is_downward_trend(data):
    ema200 = TA.EMA(data, 200)
    return data['Close'].iloc[-1] < ema200.iloc[-1]