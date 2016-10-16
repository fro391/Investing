import urllib2
import json
import datetime
import time
import pandas as pd

def getMFI (symbol):
    dt = datetime.datetime.now()
    UnixTime = int(time.mktime(dt.timetuple()))
    #https://finance-yql.media.yahoo.com/v7/finance/chart/KING?period2=1430672173&period1=1378832173&interval=1m&indicators=quote%7Cmfi~200&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com
    url='https://finance-yql.media.yahoo.com/v7/finance/chart/'+symbol+'?period2='+str(UnixTime)+'&period1='+str(UnixTime-86400*4)+'&interval=1m&indicators=quote%7Cmfi~360&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'
    #use legitimate header so bot won't pick up
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}
    request = urllib2.Request(url,headers = hdr)
    htmltext = urllib2.urlopen(request)

    try:
        #dictionaries
        data = json.load(htmltext)
        quote = data['chart']['result'][0]['indicators']['quote'][0]
        MFI = data['chart']['result'][0]['indicators']['mfi'][0]['mfi'][-1]
        timestamp = data['chart']['result'][0]['timestamp'][-1]
        df = pd.DataFrame(data={'timestamp':timestamp,'MFI':MFI},index=[symbol])
        return df

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message, symbol