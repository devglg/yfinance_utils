#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
import math
import pandas as pd

##########################
# DF Utils               #
##########################

# line : list of items in the row to add to df
def add_row_to_df(df, line, COLUMNS):
    tmp = pd.DataFrame([line], columns=COLUMNS)  
    df = pd.concat([df,tmp], ignore_index=True)
    return df