import articletext
from newspaper import Article
import threading
import timeit

#establishing lock variable
global lock
lock = threading.Lock()

def StockKeyWords(symbol):
    url = "http://www.reuters.com/finance/stocks/companyProfile?symbol="+symbol
    toBeWritten = ''
    toBeWritten += symbol + ","
    c = -1
    try:
        a = Article(url)
        a.download()
        a.parse()
        UnicodeArticle = a.text
        StringArticle = UnicodeArticle.encode('ascii','ignore')
        StrippedArticle = StringArticle.replace('\n','')
        KeyWords = articletext.getKeywords(StrippedArticle)

        for i in KeyWords:
            c += 1
            toBeWritten += KeyWords[c] + ' '
        toBeWritten += '\n'

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message, symbol
    #write variable to file if there are keywords

    if len(KeyWords) >1:
        lock.acquire()
        try:
            myfile.write(toBeWritten)
        finally:
            lock.release()

start = timeit.default_timer()
tickers = ''
threadlist = []

myfile = open('data\KeyWords.csv', 'w+')
myfile.write('symbol,Keywords'+'\n')
myfile.close()


symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')
symbolfile.close()


#open "myfile" file for SentimentRSS to write in
myfile = open('data\KeyWords'+'.csv', 'a')

for u in symbolslist:
    t = threading.Thread(target = StockKeyWords,args=(u,))
    t.start()
    threadlist.append(t)
    #sets top limit of active threads to 30
    while threading.activeCount()>30:
        a=0
    #print threading.activeCount()
#finishes threads before closing file
for b in threadlist:
    b.join()

#close file
myfile.close()

print '# of threads: ' + str(len(threadlist))
stop = timeit.default_timer()
print stop - start

