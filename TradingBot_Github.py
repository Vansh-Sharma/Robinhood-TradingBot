# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 07:59:15 2021

@author: Vansh
"""

import robin_stocks
import robin_stocks.robinhood as r
import time 
import json
import urllib
from datetime import date
from datetime import timedelta
import schedule

"""
TODO: 
    Add check in sellStock to prevent short selling!!!
    Consider backtesting
"""

def login(username, password):
    login = r.login(username,password)
    print("logged in")

def holdings():
    print(r.account.build_holdings(with_dividends = False))
    
def getRSIList(ticker):
    data = urllib.request.urlopen(f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=daily&time_period=14&series_type=close&apikey={your alphavantage api}")
    jdata = json.load(data)
    yday = date.today() - timedelta(days=1)
    most_recent_rsi = jdata["Technical Analysis: RSI"][f"{yday}"]["RSI"]
    return most_recent_rsi

def buyStock(ticker):
    rsi = getRSIList(ticker)
    price_bought = r.stocks.get_latest_price(ticker)
    if float (rsi) < 30:
        r.orders.order_buy_market(ticker, 1, timeInForce='gtc', 
                                   extendedHours=False, jsonify=False)
        print(f"Currently bought: {ticker} for {price_bought} at RSI: {rsi}")
    else:
        print(f"Did not purchase {ticker}")
        
def sellStock(ticker):
    rsi = getRSIList(ticker)
    #Need to include check if stock is in portfolio - no short selling
    price_sold = r.stocks.get_latest_price(ticker)
    if float (rsi) > 70:
        r.orders.order_sell_market(ticker, 1, timeInForce='gtc',
                                  extendedHours=False, jsonify=False)
        print(f"Currently sold: {ticker} for {price_sold} at RSI: {rsi}")
    else:
        print(f"Did not sell {ticker}")

def main():
    username = "xxx"
    password = "xxx"
    login(username, password)
    #Cancels orders from previous day
    r.orders.cancel_all_stock_orders()
    #Supply all stocks that should be looked at
    stocks = ['GNUS']
    for stock in stocks:
        print(getRSIList(f'{stock}'))
        buyStock(f'{stock}')
        sellStock(f'{stock}')
    print(r.orders.get_all_open_stock_orders())

def trial():
    #Used to test if scheduler is working
    print("working")

if __name__ == '__main__':
    schedule.every().day.at("07:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)
