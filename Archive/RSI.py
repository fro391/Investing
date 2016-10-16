import urllib
import threading
import timeit
import stockretriever

global lock
lock = threading.Lock()

def getRSI (symbol):
    url = "https://chartapi.finance.yahoo.com/instrument/1.0/"+symbol+"/chartdata;type=rsi;ys=2014;yz=2;ts=1234567890/csv?period=14"
    htmltext = urllib.urlopen(url).read()
    stockinfo = stockretriever.get_current_info([symbol])
    try:
        LastPrice = stockinfo['LastTradePriceOnly']
        if not 'message' in str(htmltext.split('\n')[-2]) and not 'alternate_ranges:' in str(htmltext.split('\n')[-2]):
            toBeWritten = str(symbol) + "," + str(htmltext.split('\n')[-2])+','+ str(LastPrice)+'\n'
            lock.acquire()
            try:
                myfile.write(toBeWritten)
            finally:
                lock.release()
    except:
        pass

#start timer
start = timeit.default_timer()

symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')

threadlist = []

#creating file in local directory
myfile = open('RSI.csv', 'w+')
myfile.write('Ticker, Date, RSI14,Price'+'\n')
myfile.close()

#threading to append info into csv
myfile = open('RSI.csv', 'a')

for u in symbolslist:

    t = threading.Thread(target = getRSI,args=(u,))
    t.start()
    threadlist.append(t)
    #sets top limit of active threads to 100
    while threading.activeCount()>100:
        a=0
    #print threading.activeCount()

for b in threadlist:
    b.join()

print len(threadlist)

myfile.close()
#timer
stop = timeit.default_timer()
print "start= ",start,"stop= ",stop, "total= ", stop-start