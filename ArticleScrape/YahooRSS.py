import threading
import RSS_URL
from newspaper import Article
from vaderSentiment import vaderSentiment

#setting lock variable for threading
global lock
lock = threading.Lock()

def SentimentRSS (symbol):

    url = "http://feeds.finance.yahoo.com/rss/2.0/headline?s="+symbol+"&region=US&lang=en-US"
    #gets list of links from above RSS feed
    NewsURLs = RSS_URL.getURLs2(url)

    #String to be written to file
    toBeWrittenToFile = ''

    for link in NewsURLs:
        try:
            #gets article portion of the htmltext
            a = Article(link)
            a.download()
            a.parse()

            #not working if it's RSS title link or has no title or cannot be accessed
            if not 'Stock - Yahoo! Finance' in a.title and not '400 Bad Request' in a.title and not '403 Forbidden' in a.title and a.title != '':
                UnicodeArticle = a.text
                StringArticle = UnicodeArticle.encode('ascii','ignore')
                StrippedArticle = StringArticle.replace('\n','')

                #remove ascii symbols
                ArticleTitle = a.title.encode('ascii','ignore').replace(',','')

                #writes sentiment from sentiment API to file
                #locks this block so that only one thread can write to file at a time

                #vader sentiment dictionary
                s = vaderSentiment.sentiment(StrippedArticle)

                #not writing articles with zero sentiments
                #collect a string to be written to file
                if s['compound'] != 0:
                    print ArticleTitle
                    toBeWrittenToFile += (str(symbol)+','+ str(s['neg'])+','+ str(s['neu'])+','+str(s['pos'])+','+ str(s['compound'])+','+ ArticleTitle +','+ str(link) +'\n')

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message

    lock.acquire()
    try:
        myfile.write(toBeWrittenToFile)
    finally:
        lock.release()