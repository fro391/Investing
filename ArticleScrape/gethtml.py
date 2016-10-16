import mechanize
import urllib2


def getHtmlText(url):
        # setup your header, add anything you want
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(url,headers = hdr)
        page = urllib2.urlopen(request)
        htmltext = page.read()
        '''
        br = mechanize.Browser()
        htmltext = br.open(url).read()
        '''
        return htmltext
    except:
        return "error"

def getHtmlFile(url):
    br = mechanize.Browser()
    htmltext = br.open(url)
    return htmltext



