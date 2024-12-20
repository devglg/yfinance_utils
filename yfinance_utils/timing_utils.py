import time

def start(lst):
    print('')
    print('')
    print('***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***')
    print('')
    print(f'Working with {len(lst)} companies')
    print('')
    return time.time()

def end(start):
    print('')
    print("TIMING")
    end_time = time.time()
    print(f"time: script took {round((end_time - start)/60, 1)} minutes")
    print('')
    print('^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^')
    print('')
    print('')