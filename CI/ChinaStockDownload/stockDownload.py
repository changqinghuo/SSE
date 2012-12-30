import datetime as dt
import threading
from stock_thread import *
import codecs
from Queue import Queue

global symbols
global error_symbols


update_filename = 'chinastock.txt'
error_log = "errlog.txt"
symbols = Queue()
error_symbols = Queue()

def get_update_symbols(updatefile):
    symbols = Queue()
    with open(updatefile, 'r')as f:
            for line in f:
                symbols.put(line.split(',')[0].strip())
    return symbols
def get_error_symbols(error_log):
    symbols = Queue()
    with open(error_log, 'r')as f:
            for line in f:
                sym = line.split(',')[0].strip()
                if sym != "":
                    symbols.put(sym)
    return symbols
def main(num):
    global error_symbols
    mylock = threading.RLock()
    startday = dt.datetime(2000, 1, 1)
    endday = dt.datetime.now() - dt.timedelta(days=1)
   # startday = dt.datetime(2012,12,31)
   # endday = dt.datetime(2012,12,31)
    endday = dt.datetime(endday.year, endday.month, endday.day)
    symbols = get_update_symbols(update_filename)
    max_count = 0
    thread_list = []
    while not symbols.empty() and max_count < 5:
        error_symbols = Queue()
        max_count += 1
        thread_list = []
        for i in range(num):
            t = StockDataUpdateThread(symbols, startday, endday,error_symbols)
            thread_list.append(t)
            t.start()
        for t in thread_list:
            t.join()
        symbols = error_symbols
    with open(error_log, 'w') as f:
        while not error_symbols.empty():
            f.write(error_symbols.get()+"\n")


if __name__ == '__main__':
    main(3)

