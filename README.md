# yfinance_utils
Just adding some utilities to the yfinance library to make it easier to do technical analysis on any stock. maybe run models and do ad-hoc scenarios.
This is mostly in response to a request from my friend Chris that I had a discussion with about fundamental and technical analysis being part of 
Finance not Accounting. This is not Accounting, Chris, we're not closing books, or creating financial statements, this is analysis of data, so definitely 
not Accounting. There is no class in Accounting about this type of analysis. *And if it is, then, there should be a class in the accounting program that teaches this.*
I mean, anyone can learn anything if they are taught it.

- **Investors be like: "Fundamental Analysis is the only way"**

- **Traders be like: "Technical Analysis is the only way"**

- **Real life be like: "Trump won with Elon financing..."**
![tesla](https://github.com/devglg/yfinance_utils/blob/main/assets/images/tsla.png)

> "There are two methods in software design. One is to make the program so complicated that there are no obvious errors. The other is to do it so simple that there are obviously no errors". This is meant to be the latter.

> [!IMPORTANT]
> Some files still have the old apache 2 license text. they are not, this whole project is GPL3 licensed, not apache 2. Could have used a little more planning.

> [!NOTE]
> After learnings enough about dataframes, matplotlib, pandas, and technical analysis, I would say that you're probably better off using yfinance, plotly, 
> and FINTA to create models instead of having to re-write everything from scratch. However, I think it is beneficial to do it manually until you understand 
> it before you start using someone else's libraries.


> [!NOTE]
> added the scripts i'm testing this with. Use at your own peril :/ you will need to create the folders `datasets` and `out`. datasets will hold the
> downloaded data from yfinance and out will hold the output of the scripts

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

### install the module (you don't plan to edit the library)
`.\venv\Scripts\pip.exe install .`

### install the module (you plan to edit the library)
`.\venv\Scripts\pip.exe install -e .`

### install requirements
`.\venv\Scripts\pip.exe install -r requirements.txt`

## does it work?

If you've worked with R you may find it very similar. It may even be the using the same libraries but I just touched R for a couple of weeks
and I didn't do much with it other than plotting and data extraction.

### open the command line
```
> .\venv\Scripts\python.exe 
>>> import warnings
>>> warnings.filterwarnings("ignore")
>>> import yfinance
>>> from yfinance_utils import rsi_utils
>>> tick = yfinance.Ticker("AMD")
>>> tick.history()
>>> tick.history()
                                 Open        High         Low       Close    Volume  Dividends  Stock Splits
Date
2024-10-30 00:00:00-04:00  153.009995  153.119995  148.100006  148.600006  87701700        0.0           0.0
2024-10-31 00:00:00-04:00  147.800003  148.679993  143.330002  144.070007  44386600        0.0           0.0
2024-11-01 00:00:00-04:00  144.440002  144.539993  141.320007  141.860001  39027400        0.0           0.0
2024-11-04 00:00:00-05:00  141.699997  143.639999  139.720001  140.710007  29117400        0.0           0.0
2024-11-05 00:00:00-05:00  141.940002  143.080002  140.800003  141.660004  27067300        0.0           0.0
2024-11-06 00:00:00-05:00  144.949997  145.630005  141.520004  145.100006  32911500        0.0           0.0
2024-11-07 00:00:00-05:00  146.679993  150.119995  145.660004  149.820007  30326400        0.0           0.0
2024-11-08 00:00:00-05:00  149.389999  150.710007  147.529999  147.949997  27560300        0.0           0.0
2024-11-11 00:00:00-05:00  147.380005  148.570007  144.910004  147.350006  29868100        0.0           0.0
2024-11-12 00:00:00-05:00  147.000000  147.449997  141.550003  143.630005  33560300        0.0           0.0
2024-11-13 00:00:00-05:00  142.860001  144.490005  139.070007  139.300003  35146600        0.0           0.0
2024-11-14 00:00:00-05:00  140.339996  141.399994  138.559998  138.839996  31681400        0.0           0.0
2024-11-15 00:00:00-05:00  136.570007  137.350006  133.649994  134.899994  44217500        0.0           0.0
2024-11-18 00:00:00-05:00  138.190002  140.899994  137.210007  138.929993  38782400        0.0           0.0
2024-11-19 00:00:00-05:00  137.410004  139.750000  137.139999  139.389999  23131400        0.0           0.0
2024-11-20 00:00:00-05:00  138.960007  140.770004  135.479996  137.600006  28843100        0.0           0.0
2024-11-21 00:00:00-05:00  138.869995  140.279999  134.929993  137.490005  29311400        0.0           0.0
2024-11-22 00:00:00-05:00  137.350006  139.130005  137.039993  138.350006  21784700        0.0           0.0
2024-11-25 00:00:00-05:00  140.490005  142.350006  139.050003  141.130005  30923100        0.0           0.0
2024-11-26 00:00:00-05:00  142.550003  142.800003  136.619995  137.720001  32092400        0.0           0.0
2024-11-27 00:00:00-05:00  137.199997  137.940002  132.960007  136.240005  30175300        0.0           0.0
2024-11-29 00:00:00-05:00  136.240005  138.589996  135.779999  137.179993  16085700        0.0           0.0

>>> data = rsi_utils.get_rsi(tick)

...ignore the warnings...

>>> print(data)
                                 Open        High         Low       Close    Volume  Dividends  Stock Splits        rsi
Date
2024-10-30 00:00:00-04:00  153.009995  153.119995  148.100006  148.600006  87701700        0.0           0.0        NaN
2024-10-31 00:00:00-04:00  147.800003  148.679993  143.330002  144.070007  44386600        0.0           0.0        NaN
2024-11-01 00:00:00-04:00  144.440002  144.539993  141.320007  141.860001  39027400        0.0           0.0        NaN
2024-11-04 00:00:00-05:00  141.699997  143.639999  139.720001  140.710007  29117400        0.0           0.0        NaN
2024-11-05 00:00:00-05:00  141.940002  143.080002  140.800003  141.660004  27067300        0.0           0.0        NaN
2024-11-06 00:00:00-05:00  144.949997  145.630005  141.520004  145.100006  32911500        0.0           0.0        NaN
2024-11-07 00:00:00-05:00  146.679993  150.119995  145.660004  149.820007  30326400        0.0           0.0        NaN
2024-11-08 00:00:00-05:00  149.389999  150.710007  147.529999  147.949997  27560300        0.0           0.0        NaN
2024-11-11 00:00:00-05:00  147.380005  148.570007  144.910004  147.350006  29868100        0.0           0.0        NaN
2024-11-12 00:00:00-05:00  147.000000  147.449997  141.550003  143.630005  33560300        0.0           0.0        NaN
2024-11-13 00:00:00-05:00  142.860001  144.490005  139.070007  139.300003  35146600        0.0           0.0        NaN
2024-11-14 00:00:00-05:00  140.339996  141.399994  138.559998  138.839996  31681400        0.0           0.0        NaN
2024-11-15 00:00:00-05:00  136.570007  137.350006  133.649994  134.899994  44217500        0.0           0.0        NaN
2024-11-18 00:00:00-05:00  138.190002  140.899994  137.210007  138.929993  38782400        0.0           0.0        NaN
2024-11-19 00:00:00-05:00  137.410004  139.750000  137.139999  139.389999  23131400        0.0           0.0  37.352376
2024-11-20 00:00:00-05:00  138.960007  140.770004  135.479996  137.600006  28843100        0.0           0.0  35.474227
2024-11-21 00:00:00-05:00  138.869995  140.279999  134.929993  137.490005  29311400        0.0           0.0  35.356573
2024-11-22 00:00:00-05:00  137.350006  139.130005  137.039993  138.350006  21784700        0.0           0.0  37.112664
2024-11-25 00:00:00-05:00  140.490005  142.350006  139.050003  141.130005  30923100        0.0           0.0  42.546084
2024-11-26 00:00:00-05:00  142.550003  142.800003  136.619995  137.720001  32092400        0.0           0.0  38.187679
2024-11-27 00:00:00-05:00  137.199997  137.940002  132.960007  136.240005  30175300        0.0           0.0  36.442775
2024-11-29 00:00:00-05:00  136.240005  138.589996  135.779999  137.179993  16085700        0.0           0.0  38.368962
```

>[!CAUTION] 
>TODO: I uploaded this manually, the paths may be wrong, need to update as soon as I can.
>Some stuff may be working but if it is not, just post some message or you can fix it and send me the pull requrest.
