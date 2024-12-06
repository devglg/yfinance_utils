from types import SimpleNamespace

def get_constants():
    CONSTANTS = {
        'MINIMUM_PRICE':10.0
    }
    return SimpleNamespace(**CONSTANTS)
