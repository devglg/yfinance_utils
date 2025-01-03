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
db = client['market']
collection = db['bigdata']

def get_all_data_from_script(script, filter = {}, columns = {}):
    filter['script']=script
    return collection.find(filter,columns).to_list()

res = get_all_data_from_script('daily_upgrades', 
                               {}, 
                               {'_id':0, 'TOTAL':1, 'UP':1,'DOWN':1,'HOLD':1, 'TICK':1,'AVG':1})


df = pd.DataFrame(res)
df = df.sort_values(by='UP', ascending=False)

fig = make_subplots(rows=1, cols=1, subplot_titles=("UPGRADES"))

fig.append_trace(go.Scatter(x=df['TICK'], y=df['UP'], mode='markers', marker=dict(size=5, color='blue'), name='UP'), row=1, col=1)
fig.append_trace(go.Scatter( x=df['TICK'], y=df['HOLD'], mode='markers', marker=dict(size=5, color='black'), name='HOLD'), row=1, col=1)
fig.append_trace(go.Scatter(x=df['TICK'], y=df['DOWN'], mode='markers', marker=dict(size=5, color='red'), name='DOWN'), row=1, col=1)

for i, row in df.iterrows():
    fig.add_shape(
        dict(type="line",
                x0=row["TICK"],
                x1=row["TICK"],
                y0=0,
                y1=row["DOWN"],
                line=dict(
                color="red",
                width=2)
            ),row=1, col=1
    )
    fig.add_shape(
        dict(type="line",
                x0=row["TICK"],
                x1=row["TICK"],
                y0=row["DOWN"],
                y1=row["HOLD"],
                line=dict(
                color="black",
                width=2)
            ),row=1, col=1
    )
    fig.add_shape(
        dict(type="line",
                x0=row["TICK"],
                x1=row["TICK"],
                y0=row["HOLD"],
                y1=row["UP"],
                line=dict(
                color="blue",
                width=2)
            ),row=1, col=1
    )


# fig.append_trace(go.Scatter(x=df2['TICK'], y=df2['DOWN'], mode='markers', marker=dict(size=5, color='red'), name='DOWNGRADE DOWN'), row=2, col=1)
# fig.append_trace(go.Scatter( x=df2['TICK'], y=df2['HOLD'], mode='markers', marker=dict(size=5, color='black'), name='DOWNGRADE HOLD'), row=2, col=1)
# fig.append_trace(go.Scatter(x=df2['TICK'], y=df2['UP'], mode='markers', marker=dict(size=5, color='blue'), name='DOWNGRADE UP'), row=2, col=1)

# for i, row in df2.iterrows():
#     fig.add_shape(
#         dict(type="line",
#                 x0=row["TICK"],
#                 x1=row["TICK"],
#                 y0=0,
#                 y1=row["DOWN"],
#                 line=dict(
#                 color="red",
#                 width=2)
#             ),row=2, col=1
#     )
#     fig.add_shape(
#         dict(type="line",
#                 x0=row["TICK"],
#                 x1=row["TICK"],
#                 y0=row["DOWN"],
#                 y1=row["HOLD"],
#                 line=dict(
#                 color="black",
#                 width=2)
#             ),row=2, col=1
#     )
#     fig.add_shape(
#         dict(type="line",
#                 x0=row["TICK"],
#                 x1=row["TICK"],
#                 y0=row["HOLD"],
#                 y1=row["UP"],
#                 line=dict(
#                 color="blue",
#                 width=2)
#             ),row=2, col=1
#     )

fig.show()