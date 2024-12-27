#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Lehi Gracia
#

# https://corporatefinanceinstitute.com/resources/accounting/financial-ratios/

from yfinance_utils import financials_utils as fu
import math

###
### GENERAL
###


## TODO: COR should be changed to COGS
def get_net_revenue(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    return ist["TotalRevenue"] - ist["CostOfRevenue"]

def get_net_income(tick, period = 0):
    return get_net_revenue(tick, period)


def get_net_sales(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    COGS = ist["CostOfRevenue"] \
            - ist["SellingGeneralAndAdministration"] \
            - ist["SellingAndMarketingExpense"] \
            - ist["GeneralAndAdministrativeExpense"] \
            - ist["OtherGandA"] \
            - ist['ResearchAndDevelopment']
    return ist["TotalRevenue"] - COGS


def get_avg_assets(tick, period = 0):
    bs = fu.get_bs(tick, period = period)
    bs1 = fu.get_bs(tick, period = period + 1)
    avg_assets = (bs["TotalAssets"] + bs1["TotalAssets"]) / 2
    return avg_assets

def get_avg_inventory(tick, period = 0):
    bs = fu.get_bs(tick, period=period)
    bs1 = fu.get_bs(tick, period=period + 1)
    avg_inventory = (bs["Inventory"] + bs1["Inventory"]) / 2
    return avg_inventory


###
### LIQUIDITY RATIOS: ability to repay both short- and long-term obligations
###

### company’s ability to pay off short-term liabilities with current assets###
def get_current_ratio(tick):
    return tick.info["currentRatio"]

### company’s ability to pay off short-term liabilities with quick assets###
def get_acid_test_ratio(tick, period = 0):
    bs = fu.get_bs(tick, period=period)
    acid = bs["CurrentAssets"] - bs["Inventory"]
    return acid / bs["CurrentLiabilities"]
    
### company’s ability to pay off short-term liabilities with cash and cash equivalents###
def get_cash_ratio(tick, period = 0):
    bs = fu.get_bs(tick, period = period)
    return bs["CashAndCashEquivalents"] / bs["CurrentLiabilities"]

### number of times a company can pay off current liabilities with the cash generated in a given period###
def get_operating_cash_flow_ratio(tick, period = 0):
    bs = fu.get_bs(tick, period = period)
    cf = fu.get_cashflow(tick, period = period)
    return cf["OperatingCashFlow"] / bs["CurrentLiabilities"]


###
### LEVERAGE RATIOS: amount of capital that comes from debt
###

### assets that are provided from debt###
def get_debt_ratio(tick, period = 0):
    bs = fu.get_bs(tick, period = period)
    return bs["TotalLiabilitiesNetMinorityInterest"] / bs["TotalAssets"]

### weight of total debt and financial liabilities against shareholders’ equity###
def get_debt_to_equity_ratio(tick, period = 0):
    bs = fu.get_bs(tick, period = period)
    return bs["TotalLiabilitiesNetMinorityInterest"] / bs["StockholdersEquity"]

### company can pay its interest expenses###
def get_interest_coverage_ratio(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    return ist["OperatingIncome"] / ist["InterestExpense"]

### company can pay its debt obligations###
def get_service_coverage_ratio(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    bs = fu.get_bs(tick, period = period)
    return ist["OperatingIncome"] / bs["TotalDebt"]


###
### EFFICIENCY RATIOS: how well a company is utilizing its assets and resources
###

### ability to generate sales from assets###
def get_asset_turnover_ratio(tick, period = 1):
    avg_assets = get_avg_assets(tick, period = period)
    net_revenue = get_net_revenue(tick, period = period)
    return net_revenue / avg_assets

### how many times a company’s inventory is sold and replaced ###
def get_inventory_turnover_ratio(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    avg_inventory = get_avg_inventory(tick, period = period + 1)
    return ist["CostOfRevenue"] / avg_inventory

### average number of days that a company holds on to inventory###
def get_day_sales_in_inventory_ratio(tick, period = 0):
    avg_inventory = get_avg_inventory(tick, period = period)
    return 365 / avg_inventory


###
### PROFITABILITY RATIOS: ability to generate income
###

### how much profit a company makes after paying its cost of goods sold###
# getting 1.0, this can't be right
def get_gross_margin_ratio(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    net_sales = get_net_sales(tick, period = period)
    return ist["GrossProfit"] / net_sales

### operating efficiency###
def get_operating_margin_ratio(tick, period = 0):
    ist = fu.get_is(tick, period=period)
    net_sales = get_net_sales(tick, period=period)
    return ist["OperatingRevenue"] / net_sales

### how efficiently a company is using its assets to generate profi###
def get_return_on_assets_ratio(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    bs = fu.get_bs(tick, period = period)
    return ist["NetIncome"] / bs["TotalAssets"]
    
### how efficiently a company is using its equity###
def get_return_on_equity(tick, period = 0):
    ist = fu.get_is(tick, period = period)
    bs = fu.get_bs(tick, period = period)
    return ist["NetIncome"] / bs["StockholdersEquity"]


###
### MARKET VALUE RATIOS: evaluate the share price of a company’s stock
###

### per-share value of a company based on the equity available to shareholders###
def get_book_value_per_share_ratio(tick):
    return  tick.info['bookValue']

### amount of dividends attributed to shareholders###
def get_dividend_yield_ratio(tick):
    return tick.info["dividendYield"] * 100 * 4 / tick.info["currentPrice"] 

### amount of net income earned for each share outstanding###
def get_earnings_per_share(tick, period = 0):
    ist = fu.get_is(tick, period=period)
    deps = ist["DilutedEPS"]
    return deps or math.nan

def get_revenue_per_share(tick, period = 0):
    ist = fu.get_is(tick, period=period)
    revenue = ist['TotalRevenue']
    shares = ist['DilutedAverageShares']
    rps = revenue / shares
    return rps or math.nan

### share price to its earnings per share###
def get_price_to_earnings(tick):
    earnings = get_earnings_per_share(tick)
    return tick.info["currentPrice"] / earnings or math.nan

### how much investors are willing to pay per dollar of sales for a stock
def get_price_to_sales(tick):
    revenue_per_share = get_revenue_per_share(tick)
    return tick.info["currentPrice"] / revenue_per_share or math.nan

