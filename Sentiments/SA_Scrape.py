import urllib2
import re

def getSaURL (rss):
    # setup your header, add anything you want
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}

    request = urllib2.Request(rss,headers = hdr)
    page = urllib2.urlopen(request)
    RSSContent = page.read()

    regex = '<link>(.+?)</link>'
    pattern = re.compile(regex)
    links = re.findall(pattern,RSSContent)
    return links
