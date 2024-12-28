import time, datetime
from yfinance_utils import log_utils

def start(lst, log = ''):
    print('***************************************************************************************')
    print('***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***')
    print('')
    print(f'Working with {len(lst)} companies. started at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('***************************************************************************************')
    print('')
    log_utils.log(f'starting: {log}')
    return time.time()

def end(start, log = ''):
    end_time = time.time()
    log_utils.log(f'complete: {log}')
    print('')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(f'timing: script took {round((end_time - start)/60, 1)} minutes. completed at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('')
    print('^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('')
    print('')