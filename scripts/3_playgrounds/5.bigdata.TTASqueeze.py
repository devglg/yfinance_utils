#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import yfinance
from datetime import datetime, timedelta
from pymongo import MongoClient
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from finta import TA

print('****************************************************************************************************************************************************')
print("If you get a KEY error you probably don't have any data, which is unlikely, or you haven't run the daily _run.py script. Run _run.py and try again.")
print('****************************************************************************************************************************************************')

client = MongoClient('mongodb://localhost:27017/')
db = client['bigdata']
collection = db.market
today = datetime.today().strftime('%Y-%m-%d')

res = collection.find(
    {"script":"daily_ttm_squeeze", "DATE":today},
    {"_id":0, "script":0, "timestamp":0}
    )

df = pd.DataFrame(res)
df.set_index("DATE", inplace=True)

symbols = list(df['TICK'])
COLUMNS = ['Adj Close', 'Open','High','Low','Close','Volume']

fig=make_subplots(rows=len(symbols), cols=1)

data = yfinance.download(symbols, period='1y')
counter=1
for symbol in symbols:
    _d2 = pd.DataFrame()
    _d2 = data.loc[:,(slice(None),symbol)]
    _d2.columns = COLUMNS
    _d2 = pd.concat([_d2, TA.BBANDS(_d2)], axis=1)
    _d2.reset_index(inplace=True)
    fig.add_trace(
        go.Scatter(y=_d2['Close'], x=_d2['Date'], name=symbol),
        secondary_y=False,
        row=counter, col=1
    )
    fig.add_trace(
        go.Scatter(y=_d2['BB_UPPER'], x=_d2['Date'], name=f'BBU'),
        secondary_y=False,
        row=counter, col=1
    )
    fig.add_trace(
        go.Scatter(y=_d2['BB_LOWER'], x=_d2['Date'], name=f'BBL'),
        secondary_y=False,
        row=counter, col=1
    )
    counter = counter + 1
fig.update_traces(mode='lines',line_shape='spline')
fig.update_layout(height=4000)
fig.show()