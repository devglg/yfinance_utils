#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

# https://corporatefinanceinstitute.com/resources/accounting/financial-ratios/

from yfinance_utils import financials_utils as fu, options_utils
import math

###
### GENERAL
###


## TODO: COR should be changed to COGS
def get_net_revenue(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
    except Exception as e:
        return math.nan
    return ist['NetIncome']

def get_net_income(tick, period = 0):
    return get_net_revenue(tick, period)


def get_net_sales(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
        sales_expenses = ist['CostOfRevenue'] \
                - ist['SellingGeneralAndAdministration'] \
                - ist['GeneralAndAdministrativeExpense'] \
                - ist['OtherGandA'] \
                - ist['ResearchAndDevelopment'] \
                - ist['SellingAndMarketingExpense']
    except Exception as e:
        return math.nan
    return ist['TotalRevenue'] - sales_expenses


def get_avg_assets(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period = period)
        bs1 = fu.get_bs(tick, period = period + 1)
        avg_assets = (bs['TotalAssets'] + bs1['TotalAssets']) / 2
    except Exception as e:
        return math.nan
    return avg_assets

def get_avg_inventory(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period=period)
        bs1 = fu.get_bs(tick, period=(period + 1))
        ratio = (bs['Inventory'] + bs1['Inventory']) / 2
    except Exception as e:
        return math.nan
    return ratio


###
### LIQUIDITY RATIOS: ability to repay both short- and long-term obligations
###

### company’s ability to pay off short-term liabilities with current assets###
def get_current_ratio(tick):
    try:
        cr = tick.info['currentRatio']
    except Exception as e:
        return math.nan
    return cr

### company’s ability to pay off short-term liabilities with quick assets###
def get_acid_test_ratio(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period=period)
        acid = bs['CurrentAssets'] - bs['Inventory']
    except Exception as e:
        return math.nan
    return acid / bs['CurrentLiabilities']
    
### company’s ability to pay off short-term liabilities with cash and cash equivalents###
def get_cash_ratio(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period = period)
    except Exception as e:
        return math.nan
    return bs['CashAndCashEquivalents'] / bs['CurrentLiabilities']

### number of times a company can pay off current liabilities with the cash generated in a given period###
def get_operating_cash_flow_ratio(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period = period)
        cf = fu.get_cashflow(tick, period = period)
    except Exception as e:
        return math.nan
    return cf['OperatingCashFlow'] / bs['CurrentLiabilities']


###
### LEVERAGE RATIOS: amount of capital that comes from debt
###

### assets that are provided from debt###
def get_debt_ratio(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period = period)
        ratio = bs['TotalLiabilitiesNetMinorityInterest'] / bs['TotalAssets']
    except Exception as e:
        return math.nan
    return ratio

### weight of total debt and financial liabilities against shareholders’ equity###
def get_debt_to_equity_ratio(tick, period = 0):
    try:
        bs = fu.get_bs(tick, period = period)
        ratio = bs['TotalLiabilitiesNetMinorityInterest'] / bs['StockholdersEquity']
    except Exception as e:
        return math.nan
    return ratio

### company can pay its interest expenses###
def get_interest_coverage_ratio(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
        ratio = ist['OperatingIncome'] / ist['InterestExpense']
    except Exception as e:
        return math.nan
    return ratio

### company can pay its debt obligations###
def get_service_coverage_ratio(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
        bs = fu.get_bs(tick, period = period)
        ratio = ist['OperatingIncome'] / bs['TotalDebt']
    except Exception as e:
        return math.nan
    return ratio


###
### EFFICIENCY RATIOS: how well a company is utilizing its assets and resources
###

### ability to generate sales from assets###
def get_asset_turnover_ratio(tick, period = 1):
    try:
        avg_assets = get_avg_assets(tick, period = period)
        net_revenue = get_net_revenue(tick, period = period)
        ratio = net_revenue / avg_assets
    except Exception as e:
        return math.nan
    return ratio

### how many times a company’s inventory is sold and replaced ###
def get_inventory_turnover_ratio(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
        avg_inventory = get_avg_inventory(tick, period = period + 1)
        ratio = ist['CostOfRevenue'] / avg_inventory
    except Exception as e:
        return math.nan
    return ratio

### average number of days that a company holds on to inventory###
def get_day_sales_in_inventory_ratio(tick, period = 0):
    try:
        avg_inventory = get_avg_inventory(tick, period = period)
        ratio = 365 / avg_inventory
    except Exception as e:
        return math.nan
    return ratio


###
### PROFITABILITY RATIOS: ability to generate income
###

### how much profit a company makes after paying its cost of goods sold###
# getting 1.0, this can't be right
def get_gross_margin_ratio(tick, period = 0):
    try:
        ist = fu.get_is(tick, period = period)
        net_sales = get_net_sales(tick, period = period)
        ratio = ist['GrossProfit'] / net_sales
    except Exception as e:
        return math.nan
    return ratio

### operating efficiency###
def get_operating_margin_ratio(tick, period = 0):
    try:
        ist = fu.get_is(tick, period=period)
        net_sales = get_net_sales(tick, period=period)
        ratio = ist['OperatingRevenue'] / net_sales
    except Exception as e:
        return math.nan
    return ratio

### how efficiently a company is using its assets to generate profi###
def get_return_on_assets_ratio(tick, period = 0):
    try:
        ni = get_net_income(tick, period)
        bs = fu.get_bs(tick, period = period)
        ratio = ni / bs['TotalAssets']
    except Exception as e:
        return math.nan
    return ratio
    
### how efficiently a company is using its equity###
def get_return_on_equity(tick, period = 0):
    try:
        ni = get_net_income(tick, period)
        bs = fu.get_bs(tick, period = period)
        ratio = ni / bs['StockholdersEquity']
    except Exception as e:
        return math.nan
    return ratio


###
### MARKET VALUE RATIOS: evaluate the share price of a company’s stock
###

### per-share value of a company based on the equity available to shareholders###
def get_book_value_per_share_ratio(tick):
    try:
        bv = tick.info['bookValue']
    except Exception as e:
        return math.nan
    return  bv

### amount of dividends attributed to shareholders###
def get_dividend_yield_ratio(tick):
    try:
        ratio = tick.info['dividendYield'] * 100 * 4 / tick.info['currentPrice']
    except Exception:
        return math.nan
    return  ratio

### amount of net income earned for each share outstanding###
def get_earnings_per_share(tick, period = 0):
    try:
        ist = fu.get_is(tick, period=period)
        deps = ist['DilutedEPS']
    except Exception as e:
        return math.nan
    return deps

def get_revenue_per_share(tick, period = 0):
    try:
        ist = fu.get_is(tick, period=period)
        revenue = ist['TotalRevenue']
        shares = ist['DilutedAverageShares']
        rps = revenue / shares
    except Exception:
        return math.nan
    return rps

### share price to its earnings per share###
def get_price_to_earnings(tick, period=0):
    try:
        earnings = get_earnings_per_share(tick)
        ratio = tick.info['currentPrice'] / earnings
    except Exception:
        return math.nan
    return ratio

### how much investors are willing to pay per dollar of sales for a stock
def get_price_to_sales(tick, period=0):
    try:
        revenue_per_share = get_revenue_per_share(tick)
        ratio = tick.info['currentPrice'] / revenue_per_share
    except Exception:
        return math.nan
    return ratio

### puts over calls show the sentiment from whales ###
def get_put_call_ratio(tick):
    calls = options_utils.get_calls_volume(tick)
    puts = options_utils.get_puts_volume(tick)
    ratio = round(puts/calls,2)
    if math.isnan(calls) or math.isnan(puts):
        return math.nan 
    return ratio

