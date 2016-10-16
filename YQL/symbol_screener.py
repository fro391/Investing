from bs4 import BeautifulSoup
import mechanize
import threading

global lock
lock = threading.Lock()

def filter (symbol):
    #collecting descriptions from rss feed
    d = []
    #list of symbols to delete
    delete = []
    url = 'http://feeds.finance.yahoo.com/rss/2.0/headline?s='+symbol+'&region=US&lang=en-US'
    br = mechanize.Browser()
    htmltext = br.open(url).read()
    soup = BeautifulSoup(htmltext)
    for desc in soup.findAll('description'):
        d.append(desc.contents)
    if 'RSS feed not found' in str(d[0]):
        lock.acquire()
        try:
                s = open("symbolsAlt.txt").read()
                s = s.replace(symbol+'\n','')
                f = open("symbolsAlt.txt", 'w')
                f.write(s)
                f.close()
                print 'deleted: ', symbol
        except:
            pass
        finally:
            lock.release()

symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')
symbolfile.close()

threadlist = []

for i in symbolslist:
    t = threading.Thread(target = filter,args=(i,))
    t.start()
    threadlist.append(t)
    #sets top limit of active threads to 100
    while threading.activeCount()>10:
        a=0
    print threading.activeCount()
#finishes threads before closing file
for b in threadlist:
    b.join()