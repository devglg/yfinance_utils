#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

from pymongo import MongoClient
from pprint import pprint
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['market']
collection = db['log']

res = collection.find(
    {'timestamp': {"$regex":str(datetime.date.today())}},
    {'_id':0, 'log':1, 'script':1, 'timestamp':1}
)

for i in res.to_list():
    if i:
        pprint(i)
