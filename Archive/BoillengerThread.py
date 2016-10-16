import urllib
import json
import datetime
import time
import threading

#gets a symbol's Boiller band info from yahoo
def getBoillenger (symbol):
    dt = datetime.datetime.now()
    UnixTime = int(time.mktime(dt.timetuple()))
    url="http://finance.yahoo.com/_td_charts_api/resource/charts;comparisonTickers=;events=div%7Csplit%7Cearn;gmtz=-4;indicators=quote%7Cbollinger~20-2;period1="+str(UnixTime-86400*3)+";period2="+str(UnixTime)+";queryString=%7B%22s%22%3A%22"+symbol+"%2BInteractive%22%7D;range=1y;rangeSelected=undefined;ticker="+symbol+";useMock=false?crumb=pnSH3nTgWWX"
    htmltext = urllib.urlopen(url)

    try:
        data = json.load(htmltext)
        test = data['data']['indicators']['quote'][0]
        test2 = data['data']['indicators']['bollinger'][0]

        close = test ['close']

        BoilUpper = test2['upper']
        BoilLower = test2['lower']

        BandWidth = float(BoilUpper[-1])-float(BoilLower[-1])

        if BandWidth != 0:
            BoilPercent = (float(close[-1]) -float(BoilLower[-1]))/ BandWidth
            myfile.write((str(symbol)+','+ str(BandWidth)+','+ str(BoilUpper[-1])+','+str(close[-1])+','+ str(BoilLower[-1])+','+ str(BoilPercent)+'\n'))

    except (ValueError, TypeError, KeyError):
        pass

symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')

threadlist = []

#creating file in local directory
myfile = open('BoillengerThread.csv', 'w+')
myfile.write('Ticker, BandWidth, BoilUpper, close, BoilLower, BoilPercent'+'\n')
myfile.close()

#threading to append info into csv
myfile = open('BoillengerThread.csv', 'a')

for u in symbolslist:

    t = threading.Thread(target = getBoillenger,args=(u,))
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
