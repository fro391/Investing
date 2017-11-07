import urllib2
import json
import datetime
import time
import threading
import timeit
import pandas as pd
from time import strftime,strptime,gmtime
from email.mime.text import MIMEText
import smtplib

'''#get email
with open('C:\\Users\\Richard\\Desktop\\Python\\hotmail.txt', 'rb') as f:
    email_list = f.read().split(',')
emailAddress = email_list[0]
password = email_list[1]

# send results to email
msg = MIMEText('Stock Analysis')
msg['Subject'] = '%s stock analysis' % str(datetime.datetime.today().strftime('%Y-%m-%d'))
msg['From'] = emailAddress
msg['To'] = emailAddress
try:
    s = smtplib.SMTP('smtp-mail.outlook.com', 25)
    s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls()  # Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(emailAddress, password)
    s.sendmail(emailAddress, emailAddress, msg.as_string())
    s.quit()
    print 'email sent to: %s' % emailAddress
except:
    raise'''

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
    url='https://finance-yql.media.yahoo.com/v7/finance/chart/'+symbol+'?period2='+str(UnixTime)+'&period1='+str(UnixTime-86400*21)+'&interval=1d&indicators=quote%7Cbollinger~20-2%7Csma~50%7Csma~20%7Csma~5%7Cmfi~14%7Cmacd~26-12-9%7Crsi~14%7Cstoch~14-1-3&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'
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
        SMA50 = data['chart']['result'][0]['indicators']['sma'][0]
        SMA20 = data['chart']['result'][0]['indicators']['sma'][1]
        SMA5 = data['chart']['result'][0]['indicators']['sma'][2]
        MFI = data['chart']['result'][0]['indicators']['mfi'][0]
        STOCH = data['chart']['result'][0]['indicators']['stoch'][0]
        LASTTRADEDATE = data['chart']['result'][0]['timestamp']

        #last trade date and last closing price
        lastTradeDate = LASTTRADEDATE [-1]
        close = quote ['close'][-1]
        opn = quote['open'][-1]
        high = quote['high'][-1]
        low= quote['low'][-1]

        vol = quote['volume'][-1]
        #Vol as percentage of avg 20 days vol
        avgV20Pct = vol / (sum(quote['volume'])/float(len(quote['volume'])))

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
        sma50 = SMA50['sma'][-1]
        sma20 = SMA20['sma'][-1]
        sma5 = SMA5['sma'][-1]

        #Avg price as percentage of sma50
        sma50pct = ((close + opn + high + low)/4) / float(sma50)

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
            toBeWritten = (str(symbol)+datetime.datetime.today().strftime('%Y%m%d')+','+ str(BandWidth)+','+ str(BoilUpper)+','+str(close)+','+str(opn)+','+str(high)+','+str(low)+','+str(avgV20Pct)+','+str(sma50pct)+','+ str(BoilLower)+','+ str(BoilPercent)+','+str(divergence)+','+str(signal)+','+str(macd)+','+str(divergencePercent)+','+str(rsi)+','+str(sma50)+','+str(sma20)+','+str(sma5)+','+str(mfi)+','+str(stochK)+','+str(stochD)+','+str(lastTradeDate)+'\n')

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
with open('iChart'+strftime("%Y-%m-%d", gmtime())+'.csv', 'w+') as myfile:
    myfile.write('Ticker&Date, BandWidth, BoilUpper, close, open, high, low, vol%, p50%, BoilLower, BoilPercent,divergence,signal,macd,divergence%,rsi,sma50,sma20,sma5,mfi,stochK,stochD,lastTradeDate'+'\n')

#threading to append info into csv
with open('iChart'+strftime("%Y-%m-%d", gmtime())+'.csv', 'a') as myfile:
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

#timer
stop = timeit.default_timer()
print "seconds of operation: " , stop - start