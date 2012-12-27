import urllib, urllib2, cookielib
import os.path
import threading
import datetime as dt
import os
import sys

data_Dir = "/home/terry/QSTK/QSData/Yahoo/"
class StockDataUpdateThread(threading.Thread):
    def __init__(self, symbols,startday, endday,errorfile_lock):
        threading.Thread.__init__(self)
        self.t_symbols = symbols
        self.t_lock = errorfile_lock
        self.t_startday = startday
        self.t_endday = endday
    def run(self):
        start_mon = self.t_startday.month
        start_day = self.t_startday.day
        start_year = self.t_startday.year
        end_mon = self.t_endday.month
        end_day = self.t_endday.day
        end_year = self.t_endday.year   
        for sym in self.t_symbols:
            stock = sym.strip()  
            print str(self), ":", sym
            filename = data_Dir + stock + '.csv'             
            bFileExist = False
            if os.path.exists(filename):
                bFileExist = True
                f_path = open(filename, 'r')
                f_content = f_path.readlines()
                f_path.close()
                str_date = f_content[1].split(',')[0].split('-')
                last_update_date = dt.datetime(int(str_date[0]), int(str_date[1]), int(str_date[2]))
                if last_update_date >= self.t_endday:
                    continue
                else: 
                    last_update_date = last_update_date + dt.timedelta(days=1)                                       
                    url = "http://ichart.finance.yahoo.com/table.csv?s=" + stock +"&a=" +\
                        str(last_update_date.month-1) + '&b='+ str(last_update_date.day) + '&c=' + str(last_update_date.year) +\
                        '&d='+str(end_mon-1)+'&e='+str(end_day)+ '&f=' + str(end_year) + "&g=d&ignore=.csv" 
            else:
                url = "http://ichart.finance.yahoo.com/table.csv?s=" + stock +"&a=" +\
                str(start_mon-1) + '&b='+ str(start_day) + '&c=' + str(start_year) +\
                '&d='+str(end_mon-1)+'&e='+str(end_day)+ '&f=' + str(end_year) + "&g=d&ignore=.csv" 

            try:             
                resp = urllib2.urlopen(url)            
                data = resp.read()
                if bFileExist: 
                    with open(filename, 'r+') as f:
                        old_content = f.readlines()
                        f.seek(0)
                        f.write(data+"".join(old_content[1:]))                                                  
                else:
                    with open(filename, 'w') as f:
                        f.write(data)   
              
            except (urllib2.HTTPError):
                logstring = stock + "," + str(sys.exc_info())+  "\n"
                self.t_lock.acquire()
                logfile = open("errlog.txt", 'a')
                logfile.write(logstring)
                logfile.close()
                self.t_lock.release()
            except:
                print  stock + "," + str(sys.exc_info())
                pass
