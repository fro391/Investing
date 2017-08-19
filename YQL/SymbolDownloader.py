#adds new found stock symbols to symbols list
import json
#first run YahooTickerDownloader.py stocks to get new symbols

#old symbols list
with open('symbols.txt','wb') as symbolfile:
    symbolslistR = symbolfile.read()
    symbolslist = symbolslistR.split('\n')
len1 = len(symbolslist)

scrappedSymbol = []

#extracting north american stocks
with open('C:\Users\Richard\Anaconda2\Scripts\Stock.json') as data_file:
    scrapefile = json.load(data_file)
for i in scrapefile:
    if '.' not in i['Ticker'] and i['Exchange']!= 'OBB'and i['Exchange']!= 'PNK'and i['Exchange']!= 'TOR'and i['Exchange']!= 'BTS'and i['Exchange']!= 'VAN':
        scrappedSymbol.append(str(i['Ticker']))
#Canadian stocks
for j in scrapefile:
    if str(j['Exchange']) == 'TOR' and str(j['Exchange']) == 'VAN':
        scrappedSymbol.append(str(j['Ticker']))

#adding new symbols to old list while removing duplicates
for t in scrappedSymbol:
    if t not in symbolslist:
        symbolslist.append(t)
len2 = len(symbolslist)

#write new list to file
symbolfile = open('symbols.txt','w+')
#counter for not adding '\n' at the last line
counter = 0
for s in symbolslist:
    counter += 1
    if counter < len(symbolslist):
        symbolfile.write(str(s)+ '\n')
    else:
        symbolfile.write(str(s))
symbolfile.close()

print "Added", len2-len1, "stocks"