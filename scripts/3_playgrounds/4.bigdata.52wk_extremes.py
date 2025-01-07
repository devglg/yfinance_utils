#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient
from plotly.subplots import make_subplots

client = MongoClient('mongodb://localhost:27017/')
db = client['bigdata']
collection = db.market

def get_all_data_from_script(script, filter = {}, columns = {}):
    filter['script']=script
    return collection.find(filter,columns).to_list()

res = collection(
                {'daily_52_week_extremes'}, 
                {'_id':0, 'TICK':1, 'PRICE':1,'HIGH':1,'LOW':1, 'VOLUME':1}
                )

df = pd.DataFrame(res)
df = df.sort_values(by='PRICE', ascending=True)

fig = make_subplots(rows=1, cols=1, subplot_titles=("EXTREMES"))

fig.append_trace(go.Scatter(x=df['TICK'], y=df['HIGH'], mode='markers', marker=dict(size=1, color='black'), name='HIGH'), row=1, col=1)
fig.append_trace(go.Scatter( x=df['TICK'], y=df['PRICE'], mode='markers', marker=dict(symbol='star', size=10, color='red'), name='PRICE'), row=1, col=1)
fig.append_trace(go.Scatter(x=df['TICK'], y=df['LOW'], mode='markers', marker=dict(size=1, color='black'), name='LOW'), row=1, col=1)

for i, row in df.iterrows():
    fig.add_shape(
        dict(type="line",
                x0=row["TICK"],
                x1=row["TICK"],
                y0=row["LOW"],
                y1=row["HIGH"],
                line=dict(
                color="black",
                width=1)
            ),row=1, col=1
    )

fig.show()