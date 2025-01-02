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

res = get_all_data_from_script('daily_analysts_up', 
                               {}, 
                               {'_id':0, 'TOTAL':1, 'GOOD':1,'BAD':1,'NEUTRAL':1, 'TICK':1,'AVG':1})

res2 = get_all_data_from_script('daily_analysts_down', 
                               {}, 
                               {'_id':0, 'TOTAL':1, 'GOOD':1,'BAD':1,'NEUTRAL':1, 'TICK':1,'AVG':1})

df = pd.DataFrame(res)
df = df.sort_values(by='GOOD', ascending=False)
df2 = pd.DataFrame(res2)
df2 = df.sort_values(by='GOOD', ascending=False)

fig = make_subplots(rows=2, cols=1)

fig.append_trace(go.Scatter(x=df['TICK'], y=df['BAD'], mode='markers', marker=dict(size=5, color='red'), name='BAD'), row=1, col=1)
fig.append_trace(go.Scatter(x=df['TICK'], y=df['GOOD'], mode='markers', marker=dict(size=5, color='blue'), name='GOOD'), row=1, col=1)
fig.append_trace(go.Scatter( x=df['TICK'], y=df['NEUTRAL'], mode='markers', marker=dict(size=5, color='red'), name='NEUTRAL'), row=1, col=1)

for i, row in df.iterrows():
    if row["NEUTRAL"]!=row["GOOD"]:
        fig.add_shape(
            dict(type="line",
                 x0=row["TICK"],
                 x1=row["TICK"],
                 y0=row["NEUTRAL"],
                 y1=row["GOOD"],
                 line=dict(
                   color="blue",
                   width=2)
                ),row=1, col=1
        )

for i, row in df.iterrows():
    if row["BAD"]!=row["NEUTRAL"]:
        fig.add_shape(
            dict(type="line",
                 x0=row["TICK"],
                 x1=row["TICK"],
                 y0=row["BAD"],
                 y1=row["NEUTRAL"],
                 line=dict(
                   color="red",
                   width=2)
                ),row=1, col=1
        )

fig.append_trace(go.Scatter(x=df2['TICK'], y=df2['BAD'], mode='markers', marker=dict(size=5, color='red'), name='BAD'), row=2, col=1)
fig.append_trace(go.Scatter(x=df2['TICK'], y=df2['GOOD'], mode='markers', marker=dict(size=5, color='blue'), name='GOOD'), row=2, col=1)
fig.append_trace(go.Scatter( x=df2['TICK'], y=df2['NEUTRAL'], mode='markers', marker=dict(size=5, color='red'), name='NEUTRAL'), row=2, col=1)

for i, row in df2.iterrows():
    if row["NEUTRAL"]!=row["GOOD"]:
        fig.add_shape(
            dict(type="line",
                 x0=row["TICK"],
                 x1=row["TICK"],
                 y0=row["NEUTRAL"],
                 y1=row["GOOD"],
                 line=dict(
                   color="blue",
                   width=2)
                ),row=2, col=1
        )

for i, row in df2.iterrows():
    if row["BAD"]!=row["NEUTRAL"]:
        fig.add_shape(
            dict(type="line",
                 x0=row["TICK"],
                 x1=row["TICK"],
                 y0=row["BAD"],
                 y1=row["NEUTRAL"],
                 line=dict(
                   color="red",
                   width=2)
                ),row=2, col=1
        )

fig.show()