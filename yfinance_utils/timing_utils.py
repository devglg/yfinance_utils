import time

def start(lst):
    print('***********************************************************************')
    print(f'Working with {len(lst)} companies')
    return time.time()

def end(start):
    print("TIMING")
    end_time = time.time()
    print(f"time: script took {round((end_time - start)/60, 1)} minutes")
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')