import datetime as dt
import threading
from stock_thread import *
import codecs



update_filename = 'chinastock.txt'
error_log = "errlog.txt"


def get_update_symbols(updatefile):
    symbols = []
    with open(updatefile, 'r')as f:
            for line in f:
                symbols.append(line.split(',')[0].strip())
    return symbols
def get_error_symbols(error_log):
    symbols = []
    with open(error_log, 'r')as f:
            for line in f:
                sym = line.split(',')[0].strip()
                if sym != "":
                    symbols.append(sym) 
    return symbols
def main(num): 
    mylock = threading.RLock()  
    startday = dt.datetime(2000, 1, 1)
    endday = dt.datetime.now() - dt.timedelta(days=1)
    endday = dt.datetime(endday.year, endday.month, endday.day)
    symbols = get_update_symbols(update_filename)
    max_count = 0
    while len(symbols) != 0 and max_count < 5:  
        max_count += 1  
        with open(error_log, 'w') as f:
            f.write("")
        thread_list = []            
        step = len(symbols)/num
        for i in range(num):
            if i != num-1:
                t = StockDataUpdateThread(symbols[i*step:(i+1)*step], startday, endday,mylock) 
            else:
                t = StockDataUpdateThread(symbols[i*step:], startday, endday,mylock) 
            thread_list.append(t)
            t.start()
        for t in thread_list:
            t.join()  
        symbols = get_error_symbols(error_log)
        
            
if __name__ == '__main__':
    main(3)            

