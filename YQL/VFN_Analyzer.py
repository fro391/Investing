import urllib2
from chunks import chunks
import threading
import timeit
from test import dataSlicing
#Doesn't work as of 2017-11-01
#establishing lock variable
global lock
lock = threading.Lock()

def VFN(symbol):
    url = 'http://finance.yahoo.com/d/quotes.csv?s='+symbol+'&f=seva2f6pol1d1m3'#symbol,EPS,volume,averageDailyV,float,lastClose,open,lastTrade,lastTradeDate,50DayMA
    #use legitimate header so bot won't pick up
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}

    request = urllib2.Request(url,headers = hdr)
    output = urllib2.urlopen(request).read()
    lock.acquire()
    try:
        myfile.write(str(output))
    finally:
        lock.release()

if __name__ == '__main__':
    start = timeit.default_timer()
    tickers = ''
    threadlist = []

    myfile = open('data\VPN.csv', 'w+')
    myfile.write('symbol,EPS,volume,averageDailyV,float,lastClose,open,lastTrade,lastTradeDate,50DayMA'+'\n')
    myfile.close()

    myfile = open('data\VPN.csv', 'a')
    #breaks symbols to chuncks of 20
    symbolfile = open("symbols.txt")
    symbolslistR = symbolfile.read()
    symbolslist = symbolslistR.split('\n')
    symbolfile.close()
    symbolChunks = list(chunks(symbolslist,100))
    for chunck in symbolChunks:
        for i in chunck:
            tickers = tickers + i + '+'
        #starting threads for every chunks
        t = threading.Thread(target = VFN,args=(tickers,))
        t.start()
        threadlist.append(t)
        #sets top limit of active threads to 50
        while threading.activeCount()>50:
            a=0
        tickers=''
    #finishes threads before closing file
    for b in threadlist:
        b.join()
    myfile.close()

    dataSlicing()

    stop = timeit.default_timer()
    print "start= ",start,"stop= ",stop