import time, datetime

def start(lst):
    print('***************************************************************************************')
    print('***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***')
    print('')
    print(f'Working with {len(lst)} companies. started at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('***************************************************************************************')
    print('')
    return time.time()

def end(start):
    end_time = time.time()
    print('')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(f'timing: script took {round((end_time - start)/60, 1)} minutes. completed at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('')
    print('^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('')
    print('')