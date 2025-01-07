# yfinance_utils
Just pounding the streets, adding some utilities to the yfinance library to make it easier for me to do technical analysis and look for trends. 
This is a pet project of mine, not doing it for school or work, so if you think is not good then ¯\_(ツ)_/¯ don't use it. Marry Christmas ❄️!!

> - **Investors be like: "Fundamental Analysis is the only way"**
> - **Traders be like: "Technical Analysis is the only way"**
> - **Real life be like: "Trump won with Elon's financing..."**
> ![tesla](https://github.com/devglg/yfinance_utils/blob/main/assets/images/tsla.png)

> [!TIP]
> "There are two methods in software design. One is to make the program so complicated that there are no obvious errors. The other is to do it so simple that there are obviously no errors". This is meant to be the latter.

## install
`git clone https://github.com/devglg/yfinance_utils.git`

### this is a python module so of course
`python -m venv venv`

### activate the python venv
`.\venv\Scripts\activate.bat`

### upgrade pip
`.\venv\Scripts\python.exe -m pip install --upgrade pip`

### install setuptools
`.\venv\Scripts\pip.exe install setuptools`

### install the module
#### if you don't plan to edit the library, run this command
`.\venv\Scripts\pip.exe install .`

#### if you plan to edit the library, run this one
`.\venv\Scripts\pip.exe install -e .`

### install requirements
`.\venv\Scripts\pip.exe install -r requirements.txt`

## does it work?

### you will need mongodb, I won't go over that but just install it locally and start it.

### open the command line
```
% ./.venv/bin/python ./scripts/snapshot.py
```

```
% YFU_PRINT_OUT=1 ./.venv/bin/python ./scripts/daily/daily_52_week_high_low.py
***************************************************************************************
***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***  START  ***

Processing 171 files. started at 2025-01-04 06:46:41
***************************************************************************************

          DATE  TICK   PRICE     HIGH     LOW    VOLUME
0   2025-01-03   CDW  171.29   261.36  171.29    947600
1   2025-01-03   PEP  150.96   182.59  150.50   5218100
2   2025-01-03  NXPI  207.30   285.39  205.64   2308100
3   2025-01-03  LUNR   19.45    19.45    2.16  22174800
4   2025-01-03  REGN  716.07  1204.72  703.90    558000
5   2025-01-03  CSGP   70.86    97.73   69.89   1848700
6   2025-01-03   TSM  204.10   205.95   99.00  10219400
7   2025-01-03   DRI  186.93   188.47  136.03   1129400
8   2025-01-03   ROP  520.66   577.50  512.00    478700
9   2025-01-03  MDLZ   59.88    76.90   59.12   7035800
10  2025-01-03  AMGN  260.00   339.00  258.00   2979700
11  2025-01-03  IDXX  410.60   578.34  406.83    341200
12  2025-01-03  CSCO   58.84    60.00   44.75  18859000
13  2025-01-03    ET   19.72    19.90   13.73  20806000
14  2025-01-03   WOR   39.16    66.37   38.50    343800
15  2025-01-03  ADBE  429.45   633.03  429.45   5617000
16  2025-01-03     V  314.18   319.77  255.39   4271300
17  2025-01-03     X   30.35    48.69   30.00  31333000

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
timing: script took 0.0 minutes. completed at 2025-01-04 06:46:41

^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^  END  ^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

# The END
