import pandas as pd
from time import gmtime, strftime

def dataSlicing():
#analyzing with pandas
    VPN = pd.read_csv('data\VPN'+'.csv').dropna()
    VPN['lastTradeDate'] = pd.to_datetime(VPN['lastTradeDate']).apply(lambda x: x.strftime('%Y%m%d'))

    #new columns being created
    VPN['Ticker&Date'] = VPN['symbol']+ VPN['lastTradeDate']
    VPN['VF%']=VPN['volume']/VPN['float']
    VPN['AvgV%']= VPN['volume']/VPN['averageDailyV']
    #   % increase in price
    VPN['priceChange'] = (VPN['lastTrade']-VPN['open'])/VPN['open']
    # 50MA%
    VPN['50MA%'] = (VPN['lastTrade']-VPN['50DayMA'])/VPN['50DayMA']

    #new df
    VPN = VPN[['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%']]

    #df for yahoo news counts
    NDY = pd.read_csv('C:\Users\Richard\Desktop\Python\Investing\ArticleScrape\data\NewsDateHist.csv')

    #df for google news counts
    NDG = pd.read_csv('C:\Users\Richard\Desktop\Python\Investing\ArticleScrape\data\NewsDateGooG.csv')

    #merge file for google and yahoo news, maxed to remove duplicates
    GYNews = NDY.append(NDG).groupby('Ticker&Date').max()
    GYNews.to_csv('C:\Users\Richard\Desktop\Python\Investing\ArticleScrape\data\GoogYahooNewsCount.csv')

    #looking up for news count on days of high volume
    YahooCount = VPN.merge(NDY, on = 'Ticker&Date', how = 'left')
    GoogleCount = VPN.merge(NDG, on = 'Ticker&Date', how = 'left')

    #take the date where the most number of news comes from either yahoo or google
    VPNout = YahooCount.append(GoogleCount).groupby('Ticker&Date').max()

    #filtering out columns
    #VPNout = VPNout.ix[VPNout['EPS']>-2,['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%','Title']]
    #VPNout = VPNout.ix[VPNout['EPS']<15,['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%','Title']]
    #VPNout = VPNout.ix[VPNout['AvgV%']>2,['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%','Title']]
    #VPNout = VPNout.ix[VPNout['priceChange']>0,['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%','Title']]
    #VPNout = VPNout.ix[VPNout['50MA%']>0.05,['Ticker&Date','EPS','AvgV%','VF%','priceChange','50MA%','Title']]

    #Saving to file
    VPNout.to_csv('data\VPNoutput'+strftime("%Y-%m-%d", gmtime())+'.csv')
