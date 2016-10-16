import urllib2
import pandas as pd
#under construction

def VFN_Retro(symbol):
    url = 'http://ichart.finance.yahoo.com/table.csv?s='+symbol
    url2 = 'http://finance.yahoo.com/d/quotes.csv?s='+symbol+'&f=sef6d1'#Symbol,EPS,float,lastTradeDate
    #using legit header to get pass as bot
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}

    #reading first url
    request = urllib2.Request(url,headers = hdr)
    htmltext = urllib2.urlopen(request).read()
    #reading second url
    request = urllib2.Request(url2,headers = hdr)
    htmltext2 = urllib2.urlopen(request).read()

    myfile = open('data\HistRaw.csv', 'w+')
    myfile.write(htmltext)
    myfile.close()

    myfile = open('data\KeyStats.csv', 'w+')
    myfile.write(htmltext2)
    myfile.close()

    df = pd.DataFrame.from_csv('data\HistRaw.csv')
    df2 = pd.DataFrame.from_csv('data\KeyStats.csv')

    #print df
    print df2

VFN_Retro('KING')
