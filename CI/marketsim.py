
import pandas
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import sys

"""closefield = "close"
"Step1: read data"
dataobj = da.DataAccess('Yahoo')
endday = dt.datetime(2011, 12,31)
timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday, endday, timeofday)
close = dataobj.get_data(timestamps, symbols_2011, closefield)"""

"""step1 read args from command line"""
closefield = "actual_close"
cash = float(sys.argv[1])
f_trade = open(sys.argv[2], 'r')
f_result = open(sys.argv[3], 'w')
print cash
trades = []
symbols  = []
for line in f_trade:
    trade_data = line.split(',')
    item = []
    date = dt.datetime(int(trade_data[0]), int(trade_data[1]), int(trade_data[2]), 16,0)
    item.append(date)
    item.append(trade_data[3])
    item.append(trade_data[4])
    item.append(int(trade_data[5]))
    trades.append(item)
    symbols.append(trade_data[3])
print trades
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
"""step2 read history data"""
symbols.append('$SPX')
symbols = set(symbols)
dataobj = da.DataAccess('Yahoo')
timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday, endday, timeofday)
close = dataobj.get_data(timestamps, symbols, closefield)
close = (close.fillna(method='ffill')).fillna(method='backfill')

"""step 3 caculate value"""
values = {}
for item in timestamps:
    values[item] = cash

stock = {}
for sym in symbols:
    stock[sym] = 0
trade_t = startday
for i in range(len(trades)):
    t = trades[i]
    t_next = t
    if i != len(trades)-1:
        t_next = trades[i+1]
    price = close[t[1]][t[0]]
    if t[2].lower() == 'sell':
        cash += price*t[3]
        stock[t[1]] -= t[3]
    else:
        cash -= price*t[3]
        stock[t[1]] += t[3]
    trade_t = t[0]
    while trade_t <= t_next[0]:
        if not (trade_t in timestamps):
            trade_t += dt.timedelta(days=1)
            continue
        stock_value = 0
        for s in stock.keys():
            stock_value += close[s][trade_t]*stock[s]
        values[trade_t] = cash + stock_value
        trade_t += dt.timedelta(days=1)


t = trade_t
last_trade = trade_t - dt.timedelta(days=1)
while t <= endday:
    if not(t in timestamps):
        t += dt.timedelta(days=1)
        continue
    values[t] = values[last_trade]
    t += dt.timedelta(days=1)



for t in sorted(values.keys()) :
    line = str(t.year) + ','
    line += str(t.month) + ','
    line += str(t.day) +',' + str(values[t]) + '\n'
    f_result.write(line)



f_trade.close()
f_result.close()
