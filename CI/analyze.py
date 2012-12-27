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
import matplotlib.pyplot as plt
from pylab import *

bechmark = sys.argv[2]
symbols = []
symbols.append(str(bechmark))

dataobj = da.DataAccess('Yahoo')
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday, endday, timeofday)
close = dataobj.get_data(timestamps, symbols, 'close')
close = (close.fillna(method='ffill')).fillna(method='backfill')

value_file = open(sys.argv[1])
values = []
for line in value_file:
    year = int(line.split(',')[0])
    mon = int(line.split(',')[1])
    day = int(line.split(',')[2])
    value_date = dt.datetime(year, mon, day)
    if value_date >= startday and value_date < endday:
         values.append(float(line.split(',')[3]))
plt.clf()
pricedat = close.values # pull the 2D ndarray out of the pandas object
print len(pricedat)
spx_dailyret_tmp = pricedat[1:,:] / pricedat[0:-1, :] -1
spx_dailyret_tmp = np.ravel(spx_dailyret_tmp)
spx_dailyret = []
spx_dailyret.append(0)
for val in spx_dailyret_tmp:
    spx_dailyret.append(val)


#base = values[0]
#for i in range(len(values)):
#    values[i] = values[i]/base
#plt.plot(timestamps,pricedat)
#plt.plot(timestamps,values)
#symbols = ['$SPX','Vaule']
#plt.legend(symbols)
#plt.ylabel('Adjusted Close')
#plt.xlabel('Date')
#savefig('adjustedclose.pdf',format='pdf')

daily_ret = []
daily_ret.append(0)
for i in range(1,len(values)):
    daily_ret.append(values[i]/values[i-1] -1)
#print 'portfolio daily return:', np.std(daily_ret, dtype = np.float64)
print  'portfolio total return:', values[-1]/values[0]
print  'portfolio daily return std:', np.std(daily_ret )
print  'portfolio daily return mean:',np.mean(daily_ret)
print  'portfolio daily return sharp ratio:', np.sqrt(len(daily_ret))*np.mean(daily_ret)/np.std(daily_ret, dtype = float64)

print "==================="

print  '$SPX total return:', pricedat[-1]/pricedat[0]
print  '$SPX daily return std:', np.std(spx_dailyret)
print  '$SPX daily return mean:', np.mean(spx_dailyret)
print  '$SPX daily return sharp ratio:', np.sqrt(len(spx_dailyret))*np.mean(spx_dailyret)/np.std(spx_dailyret, dtype = float64)
#print 'SPX daily return:', np.std(spx_dailyret, dtype = np.float64)
