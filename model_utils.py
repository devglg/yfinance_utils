#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

import pandas as pd
import utils.financials_utils as du
import utils.ratio_utils as ru
import math

LOG=False

def get_sacks_value_stocks(t, max_price_to_sales = 1.00, max_price_to_earnings = 20.00):
    MAX_PRICE_TO_SALES = max_price_to_sales
    MAX_PRICE_TO_EARNINGS = max_price_to_earnings

    COLUMNS = ["ticker","last","pte","pts"]

    results = pd.DataFrame(columns=COLUMNS)

    for tick in t.tickers:
        last_price = du.get_last_price(t.tickers[tick])
        if not last_price or math.isnan(last_price):
            continue

        price_to_earnings = ru.get_price_to_earnings(t.tickers[tick])
        if price_to_earnings > MAX_PRICE_TO_EARNINGS or price_to_earnings < 0.00:
            continue

        price_to_sales = ru.get_price_to_sales(t.tickers[tick])
        if not price_to_sales or math.isnan(price_to_sales) or price_to_sales > MAX_PRICE_TO_SALES:
            continue

        if LOG: print(f"\n{tick},{last_price:.2f},{price_to_earnings:.2f},{price_to_sales:.2f}")

        tmp = pd.DataFrame([[tick, last_price, price_to_earnings, price_to_sales]], columns=results.columns)
        if LOG: print(f"tmp: {tmp}")

        results = pd.concat([tmp, results], ignore_index=True)
        if LOG: print(f"result: {results}")

    return results
