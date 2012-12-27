'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on March, 5, 2012

@author: Sourabh Bajaj
@contact: sourabhbajaj90@gmail.com
@summary: Event Profiler Tutorial
'''


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

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""
"Time Period Jan 1, 08 - Dec 31, 09 $5 & 2008 data = 326 $5 & 2012 data = 176 $10 & 2012 data = 461 $7 & 2008 data = 468"
# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "actual_close"
volumefield = "volume"
window = 10
output_flie = "event_orders.csv"


def findEvents(symbols, startday,endday, marketSymbol,verbose=False):

	# Reading the Data for the list of Symbols.
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)
	dataobj = da.DataAccess('Yahoo')
	if verbose:
            print __name__ + " reading data"
	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)

	# Completing the Data - Removing the NaN values from the Matrix
	#close = (close.fillna(method='ffill')).fillna(method='backfill')
	#print close['SPY'][0], close['SPY'][1]

	# Calculating Daily Returns for the Market
	#tsu.returnize0(close.values)
	SPYValues=close[marketSymbol]

	# Calculating the Returns of the Stock Relative to the Market
	# So if a Stock went up 5% and the Market rised 3%. The the return relative to market is 2%
	mktneutDM = close
	np_eventmat = copy.deepcopy(mktneutDM)
    	for sym in symbols:
		for time in timestamps:
			np_eventmat[sym][time]=np.NAN

	if verbose:
            print __name__ + " finding events"

	# Generating the Event Matrix
	# Event described is : Market falls more than 3% plus the stock falls 5% more than the Market
	# Suppose : The market fell 3%, then the stock should fall more than 8% to mark the event.
	# And if the market falls 5%, then the stock should fall more than 10% to mark the event.
    	output = open(output_flie, 'w')
	output_content = []
	for i in range(1,len(timestamps)):	
	    for symbol in symbols:
	    

	        if  close[symbol][i-1] >= 7 and close[symbol][i] < 7 : # When market fall is more than 3% and also the stock compared to market is also fell by more than 5%.
             		np_eventmat[symbol][i] = 1.0  #overwriting by the bit, marking the event
                    	buy_date = timestamps[i]
                        if i+5 < len(mktneutDM[symbol]): 
                    		sell_date = timestamps[i+5];
                        else:
                                sell_date = timestamps[-1];
			output_line = []
			output_line.append(buy_date);
			output_line.append(symbol)
			output_line.append("Buy")
                        output_line.append(100)
			output_content.append(output_line)
			output_line = []
			output_line.append(sell_date);
			output_line.append(symbol)
			output_line.append("Sell")
                        output_line.append(100)
			output_content.append(output_line)
        output_content = sorted(output_content, key = lambda x: x[0])
        for item in output_content:
	    d = item[0];         	
	    line = str(d.year) + ","+ str(d.month) + "," + str(d.day) + ","
            line += item[1] + ","
            line += item[2] + "," + str(item[3])+"\n"
            output.write(line)
			
	output.close()

	return np_eventmat


#################################################
################ MAIN CODE ######################
#################################################

#SP5002008 List
dataobj = da.DataAccess('Yahoo')
symbols_2008 = dataobj.get_symbols_from_list("sp5002008")
symbols_2008.append('SPY')
symbols_2012 = dataobj.get_symbols_from_list("sp5002012")
symbols_2012.append('SPY')
for sym in symbols_2008:
    print sym
# You might get a message about some files being missing, don't worry about it.
# You might get a message about some files being missing, don't worry about it.

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
#symbols = dataobj.get_symbols_from_list("sp5002008")
#symbols.append('SPY')
#symbols = ['HD', 'HOT', 'SPY']
#for sym in symbols:
#    print sym
#startday = dt.datetime(2008,1,1)
#endday = dt.datetime(2008,1,31)

#eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)
#eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)
#eventProfiler.study(filename="MyEventStudy_test.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)


#eventMatrix = findEvents(symbols_2008,startday,endday,marketSymbol='SPY',verbose=True)
#eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)
#eventProfiler.study(filename="MyEventStudy_2008.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')
#
#
eventMatrix = findEvents(symbols_2012,startday,endday,marketSymbol='SPY',verbose=True)
eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)
eventProfiler.study(filename="MyEventStudy_2012.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')
#
