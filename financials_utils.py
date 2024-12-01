#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import utils.constants as constants

"""
GET FINANCIAL STATEMENTS as dictionary
"""
def get_is(ticker, period = 0):
  return dict(ticker.get_income_stmt()[ticker.get_income_stmt().columns[period]])

def get_bs(ticker, period = 0):
  return dict(ticker.get_balance_sheet()[ticker.get_balance_sheet().columns[period]])

def get_cashflow(ticker, period = 0):
  return dict(ticker.get_cashflow()[ticker.get_cashflow().columns[period]])



"""
GET OTHER FINANCIAL INFORMATION
"""

def get_up_down_action(ticker):
  d = ticker.get_upgrades_downgrades()
  up = d[d.Action == "up"].shape[0]
  down = d[d.Action == "down"].shape[0]
  total = len(d)
  return {"up":up, "down":down, "total":total}



def get_historic_price(ticker, price_field = constants.CLOSE):
  d = ticker.history()
  return list(d[price_field])



def get_last_price(tick):
  d = get_historic_price(tick)
  if len(d) < 1:
    return None
  return d[-1]




