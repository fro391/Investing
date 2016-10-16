import requests

def getSentiment(text):
    url = 'http://sentiment.vivekn.com/web/text/'
    txt = {"txt" : text}
    r=requests.post(url, data=txt)
    return r.text

