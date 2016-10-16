import urllib2
import json
import pandas as pd

def dataSlice ():
    #droping na and adding date
    VPN = pd.read_csv('iChart'+'.csv').dropna()
    VPN['lastTradeDate'] = pd.to_datetime(VPN['lastTradeDate']).apply(lambda x: x.strftime('%Y%m%d'))
    #new columns being created
    VPN['Ticker&Date'] = VPN['Ticker']+ VPN['lastTradeDate']
    #new df
    VPN = VPN[['Ticker&Date', 'BandWidth', 'BoilUpper', 'close', 'BoilLower', 'BoilPercent', 'divergence','signal','macd','divergence%','rsi','sma60','sma20','sma5','mfi','stochK','stochD']]

    #df for yahoo news counts
    NDY = pd.read_csv('C:\Users\SUSAN\Desktop\Python\Investing\ArticleScrape\data\NewsDateHist.csv')
    #df for google news counts
    NDG = pd.read_csv('C:\Users\SUSAN\Desktop\Python\Investing\ArticleScrape\data\NewsDateGooG.csv')
    #looking up for news count on days of high volume
    YahooCount = VPN.merge(NDY, on = 'Ticker&Date', how = 'left')
    GoogleCount = VPN.merge(NDG, on = 'Ticker&Date', how = 'left')

    #take the date where the most number of news comes from either yahoo or google
    VPNout = YahooCount.append(GoogleCount).groupby('Ticker&Date').max()

    #Saving to file
    VPNout.to_csv('iChart'+'.csv')

dataSlice()
'''
url='https://finance-yql.media.yahoo.com/v7/finance/chart/KING?period2=1430672575&period1=1430326975&interval=1d&indicators=quote%7Cbollinger~20-2%7Csma~60%7Csma~20%7Csma~5%7Cmfi~14%7Cmacd~26-12-9%7Crsi~14%7Cstoch~14-1-3&includeTimestamps=true&includePrePost=false&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Connection': 'keep-alive'}

request = urllib2.Request(url,headers = hdr)
htmltext = urllib2.urlopen(request)

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


username = 'user'
password = 'pass'
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

page = urllib2.urlopen(url).read()
'''



