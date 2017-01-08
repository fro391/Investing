import urllib2
import json
import datetime
import time
import threading
import timeit
import pandas as pd
from time import strftime,strptime,gmtime

#start timer
start = timeit.default_timer()

#declare global lock object
global lock
lock = threading.Lock()

#gets a symbol's Boiller band info from yahoo
def getiChart (symbol):
    dt = datetime.datetime.now()
    UnixTime = int(time.mktime(dt.timetuple()))
    #https://finance-yql.media.yahoo.com/v7/finance/chart/KING?period2=1430672173&period1=1378832173&interval=1d&indicators=quote%7Cbollinger~20-2%7Csma~50%7Csma~50%7Csma~50%7Cmfi~14%7Cmacd~26-12-9%7Crsi~14%7Cstoch~14-1-3&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com
    url='https://finance-yql.media.yahoo.com/v7/finance/chart/'+symbol+'?period2='+str(UnixTime)+'&period1='+str(UnixTime-86400*4)+'&interval=1d&indicators=quote%7Cbollinger~20-2%7Csma~60%7Csma~20%7Csma~5%7Cmfi~14%7Cmacd~26-12-9%7Crsi~14%7Cstoch~14-1-3&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'
    #use legitimate header so bot won't pick up
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(url,headers = hdr)
        htmltext = urllib2.urlopen(request)
    except:
        pass

    try:
        #dictionaries
        data = json.load(htmltext)
        quote = data['chart']['result'][0]['indicators']['quote'][0]
        boillinger = data['chart']['result'][0]['indicators']['bollinger'][0]
        MACD = data['chart']['result'][0]['indicators']['macd'][0]
        RSI = data['chart']['result'][0]['indicators']['rsi'][0]
        SMA60 = data['chart']['result'][0]['indicators']['sma'][0]
        SMA20 = data['chart']['result'][0]['indicators']['sma'][1]
        SMA5 = data['chart']['result'][0]['indicators']['sma'][2]
        MFI = data['chart']['result'][0]['indicators']['mfi'][0]
        STOCH = data['chart']['result'][0]['indicators']['stoch'][0]
        LASTTRADEDATE = data['chart']['result'][0]['timestamp']

        #last trade date and last closing price
        lastTradeDate = LASTTRADEDATE [-1]
        close = quote ['close'][-1]

        #boillinger data
        BoilUpper = boillinger['upper'][-1]
        BoilLower = boillinger['lower'][-1]
        BandWidth = float(BoilUpper)-float(BoilLower)
        #MACD data
        divergence = MACD['divergence'][-1]
        signal = MACD ['signal'][-1]
        macd = MACD ['macd'][-1]
        #RSI data
        rsi = RSI['rsi'][-1]
        #SMA data
        sma60 = SMA60['sma'][-1]
        sma20 = SMA20['sma'][-1]
        sma5 = SMA5['sma'][-1]
        #MFI data
        mfi = MFI['mfi'][-1]
        #STOCH
        stochK = STOCH['k'][-1]
        stochD = STOCH['d'][-1]

        if BandWidth != 0:
            # percent of price in boillenger band
            BoilPercent = (float(close) -float(BoilLower))/ BandWidth
            # of divergence over close price
            divergencePercent = float(divergence)/float(close)
            #variable to be written to file. this will still process if thread is locked
            toBeWritten = (str(symbol)+datetime.datetime.today().strftime('%Y%m%d')+','+ str(BandWidth)+','+ str(BoilUpper)+','+str(close)+','+ str(BoilLower)+','+ str(BoilPercent)+','+str(divergence)+','+str(signal)+','+str(macd)+','+str(divergencePercent)+','+str(rsi)+','+str(sma60)+','+str(sma20)+','+str(sma5)+','+str(mfi)+','+str(stochK)+','+str(stochD)+','+str(lastTradeDate)+'\n')

            lock.acquire()
            try:
                myfile.write(toBeWritten)
            finally:
                lock.release()

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message, symbol


symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')

threadlist = []

#creating file in local directory
myfile = open('iChart'+strftime("%Y-%m-%d", gmtime())+'.csv', 'w+')
myfile.write('Ticker&Date, BandWidth, BoilUpper, close, BoilLower, BoilPercent,divergence,signal,macd,divergence%,rsi,sma60,sma20,sma5,mfi,stochK,stochD,lastTradeDate'+'\n')
myfile.close()

#threading to append info into csv
myfile = open('iChart'+strftime("%Y-%m-%d", gmtime())+'.csv', 'a')

for u in symbolslist:

    t = threading.Thread(target = getiChart,args=(u,))
    t.start()
    threadlist.append(t)
    #sets top limit of active threads to 50
    while threading.activeCount()>50:
        a=0
    #print threading.activeCount()

for b in threadlist:
    b.join()
print "# of threads: ", len(threadlist)
myfile.close()

#timer
stop = timeit.default_timer()
print "seconds of operation: " , stop - start