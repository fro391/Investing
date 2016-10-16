from bs4 import BeautifulSoup
import gethtml
import re
import urlparse
#gets titles
def getURLs (rss):
    Titles = []
    soup = BeautifulSoup(gethtml.getHtmlText(rss),'lxml')
    for item in soup.findAll('item'):
        #link tag cut off after stripping for item... only </link> is there
        for i in item.findAll('title'):
            try:
                Titles.append(i.contents[0])
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
    return Titles
#gets links
def getURLs2 (rss):
    htmltext = gethtml.getHtmlText(rss)
    regex = '<link>(.+?)</link>'
    pattern = re.compile(regex)
    links = re.findall(pattern,htmltext)
    #returns valid links
    goodlinks = [link for link in links if bool(urlparse.urlparse(link))==True ]
    return goodlinks
#gets dates
def getURLs3 (rss):
    htmltext = gethtml.getHtmlText(rss)
    regex = '<pubDate>(.+?)</pubDate>'
    pattern = re.compile(regex)
    date = re.findall(pattern,htmltext)
    return date

