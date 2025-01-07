#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
from pprint import pprint
from pymongo import MongoClient
import plotly.graph_objects as go
from plotly.subplots import make_subplots

client = MongoClient('mongodb://localhost:27017/')
db = client['bigdata']
collection = db['daily_volume_total']

res = collection({"TOTAL":{'$exists': 1}}, 
                 {'_id':0, 'TOTAL':1, 'META':1,'AAPL':1,'TSLA':1, 'MSFT':1,'DATE':1, 'NVDA':1}
                )
data = pd.DataFrame(res)

fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True, }]])
fig.add_trace(go.Scatter(x=data['DATE'], y=data['AAPL'], name='AAPL'), secondary_y=False,)
fig.add_trace(go.Scatter(x=data['DATE'], y=data['TSLA'], name='TSLA'), secondary_y=False,)
fig.add_trace(go.Scatter(x=data['DATE'], y=data['MSFT'], name='MSFT'), secondary_y=False,)
fig.add_trace(go.Scatter(x=data['DATE'], y=data['META'], name='META'), secondary_y=False,)
fig.add_trace(go.Scatter(x=data['DATE'], y=data['NVDA'], name='NVDA'), secondary_y=False,)
fig.add_trace(go.Scatter(x=data['DATE'], y=data['TOTAL'], name='TOTAL'), secondary_y=True,)
fig.show()
