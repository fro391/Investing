from newspaper import Article
import re

def textDownload (H_Link):
    #gets article portion of the htmltext
    try:
        a = Article(H_Link)
        a.download()
        a.parse()

        UnicodeArticle = a.text
        StringArticle = UnicodeArticle.encode('ascii','ignore')
        StrippedArticle = StringArticle.replace('\n','')
        return StrippedArticle

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message

def countKeyWords (text,keyword):
    #returns count of given keyword
    regex = keyword
    pattern = re.compile(regex,re.IGNORECASE)
    l = re.findall(pattern,text)
    return 'There are '+str(len(l))+ ' occurances of \"'+ keyword +'\" in the article.'

if __name__ == '__main__':
    keyword = 'percent' #not case sensitive
    html_link = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20170201a.htm'
    print countKeyWords(textDownload(html_link),keyword)