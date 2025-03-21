#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import time, datetime
from yfinance_utils import log_utils

def start(lst, filename, log=' '):
    print('***************************************************************************************')
    print('***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***')
    print('')
    print(f'Processing {len(lst)} files. started at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('***************************************************************************************')
    print('')
    log_utils.log(filename, f'started, {log}')
    return time.time()

def end(start, filename, log=' '):
    end_time = time.time()
    log_utils.log(filename, f'completed, {log}')
    print('')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(f'timing: script took {round((end_time - start)/60, 1)} minutes. completed at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('')
    print('^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('')
    print('')