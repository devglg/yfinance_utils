from finta import TA


def is_macd_cross_up(data):
    macd = TA.MACD(data)
    return macd['MACD'].iloc[-1] > macd['SIGNAL'].iloc[-1] and \
            macd['MACD'].iloc[-5] < macd['SIGNAL'].iloc[-5] and \
            macd['MACD'].iloc[-1] < 0.0

def is_macd_cross_down(data):
    macd = TA.MACD(data)
    return macd['MACD'].iloc[-1] < macd['SIGNAL'].iloc[-1] and \
            macd['MACD'].iloc[-5] > macd['SIGNAL'].iloc[-5] and \
            macd['MACD'].iloc[-1] > 0.0

def is_stoch_cross_up(data):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] > stochd.iloc[-1] and \
            stochk.iloc[-5] < stochd.iloc[-5] and \
            stochk.iloc[-1] > 20 and stochk.iloc[-5] < 20

def is_stoch_cross_down(data):
    stochk = TA.STOCH(data)
    stochd = TA.STOCHD(data)
    return stochk.iloc[-1] < stochd.iloc[-1] and \
            stochk.iloc[-5] > stochd.iloc[-5] and \
            stochk.iloc[-1] < 80 and stochk.iloc[-5] > 80

def is_upward_trend(data):
    ema200 = TA.EMA(data, 200)
    return data['Close'].iloc[-1] > ema200.iloc[-1]