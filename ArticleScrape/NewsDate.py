import RSS_URL
from time import strftime, strptime
from datetime import datetime, timedelta
import threading
import timeit
import pandas as pd

#setting lock variable for threading
global lock
lock = threading.Lock()

def NewsDate (symbol):
    url = "http://feeds.finance.yahoo.com/rss/2.0/headline?s="+symbol+"&region=US&lang=en-US"
    #timezone conversion variables
    #title of articles
    titles = RSS_URL.getURLs(url)
    #dates of articles
    dates = RSS_URL.getURLs3(url)
    toBeWritten = ''
    c = -1
    #writes symbol, title, and date of news articles

    if len(titles)!= len(dates):
        pass
    elif (len(titles) * len(dates)) == 0:
        pass
    else:
        try:
            for i in dates:
                #encoding article titles and replacing ","
                #using c as index for 'titles' list
                c += 1
                ArticleTitle = titles[c].encode('ascii','ignore').replace(',','')
                #accounting for time zones
                utc = datetime.strptime(i,'%a, %d %b %Y %H:%M:%S %z')
                local = utc + timedelta(hours=-5)
                #converts yahoo's timestamp to YearMonthDate
                j = strftime("%Y%m%d",strptime(str(local),"%Y-%m-%d %H:%M:%S"))
                #stores to be written variable
                toBeWritten += (str(symbol) + j+ ',' + str(ArticleTitle) +'\n')

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message, symbol
        #write variable to file
        lock.acquire()
        try:
            myfile.write(toBeWritten)
        finally:
            lock.release()

if __name__ == '__main__':
    start = timeit.default_timer()

    #creating file in local 'data' directory
    with open('data\NewsDate'+'.csv', 'w+') as myfile:
        myfile.write('Ticker&Date,Title'+'\n')

    #Getting all symbols into list
    with open("symbols.txt") as symbolfile:
        symbolslistR = symbolfile.read()
        symbolslist = symbolslistR.split('\n')

    #tracks threads running
    threadlist = []

    #open "myfile" file for SentimentRSS to write in
    with open('data\NewsDate'+'.csv', 'a') as myfile:

        for u in symbolslist:
            t = threading.Thread(target = NewsDate,args=(u,))
            t.start()
            threadlist.append(t)
            #sets top limit of active threads to 10
            while threading.activeCount()>50:
                a=0
            #print threading.activeCount()
        #finishes threads before closing file
        for b in threadlist:
            b.join()

    print '# of threads: ' + str(len(threadlist))

    #group by output by number of articles per day
    ND = pd.read_csv('data\NewsDate'+'.csv').groupby('Ticker&Date').count()
    ND.to_csv('data\NewsDate'+'.csv')

    #adds the new data to a NewsDate historical file
    NDHist = pd.read_csv('data\NewsDateHist'+'.csv',index_col = 0)
    NDHist.append(ND).to_csv('data\NewsDateHist'+'.csv')
    #use groupby max to remove duplicates
    pd.read_csv('data\NewsDateHist'+'.csv').groupby('Ticker&Date').max().to_csv('data\NewsDateHist'+'.csv')

    stop = timeit.default_timer()
    print stop - start