#news count for google rss feed
import RSS_URL
from time import strftime, strptime
from datetime import datetime, timedelta
import threading
import timeit
import pandas as pd

#setting lock variable for threading
global lock
lock = threading.Lock()

def NewsDateG (symbol):
    url = "http://www.google.ca/finance/company_news?q="+symbol+"&output=rss"
    #catching any errors in titles and dates' format
    try:
        #title of articles
        titles = RSS_URL.getURLs(url)
        #dates of articles
        dates = RSS_URL.getURLs3(url)
        #if loop for empty date ranges and title ranges
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message, symbol

    if len(titles)!= len(dates):
        pass
    elif (len(titles) * len(dates)) == 0:
        pass
    else:
        toBeWritten = ''
        c = -1
        #writes symbol, title, and date of news articles
        try:
            for i in dates:
                #encoding article titles and replacing ","
                #using c as index for 'titles' list
                c += 1
                ArticleTitle = titles[c].encode('ascii','ignore').replace(',','')
                #accounting for time zones
                utc = datetime.strptime(i,'%a, %d %b %Y %H:%M:%S %Z')
                local = utc + timedelta(hours=-5)
                #converts google's timestamp to YearMonthDate
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
    myfile = open('data\NewsDateG'+'.csv', 'w+')
    myfile.write('Ticker&Date,Title'+'\n')
    myfile.close()

    #Getting all symbols into list
    symbolfile = open("symbols.txt")
    symbolslistR = symbolfile.read()
    symbolslist = symbolslistR.split('\n')
    symbolfile.close()

    #tracks threads running
    threadlist = []

    #open "myfile" file for SentimentRSS to write in
    myfile = open('data\NewsDateG'+'.csv', 'a')

    for u in symbolslist:
        t = threading.Thread(target = NewsDateG,args=(u,))
        t.start()
        threadlist.append(t)
        #sets top limit of active threads to 10
        while threading.activeCount()>2:
            a=0
        #print threading.activeCount()
    #finishes threads before closing file
    for b in threadlist:
        b.join()

    #close file
    myfile.close()

    print '# of threads: ' + str(len(threadlist))

    #group by output by number of articles per day
    ND = pd.read_csv('data\NewsDateG'+'.csv').groupby('Ticker&Date').count()
    ND.to_csv('data\NewsDateG'+'.csv')

    #adds the new data to a NewsDate historical file
    NDHist = pd.read_csv('data\NewsDateGooG'+'.csv',index_col = 0)
    NDHist.append(ND).to_csv('data\NewsDateGooG'+'.csv')
    #use groupby max to remove duplicates
    pd.read_csv('data\NewsDateGooG'+'.csv').groupby('Ticker&Date').max().to_csv('data\NewsDateGooG'+'.csv')

    stop = timeit.default_timer()
    print stop - start