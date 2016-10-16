from bs4 import BeautifulSoup
import getsentiment
import gethtml

def getArticleText(webtext):
        articletext = ''
        soup = BeautifulSoup(webtext)
        for tag in soup.findAll('p'):
            try:
                articletext += str(tag.contents[0])
            except:
                a = 0
        return articletext

def getArticle(url):
    htmltext = gethtml.getHtmlText(url)
    return getArticleText(htmltext)

def getKeywords(articletext):
    common = open("common.txt").read().split('\n')#top 100 common words
    word_dict = {}
    word_list = articletext.lower().split()#change to lower case
    for word in word_list:
        if word not in common and word.isalnum():#not common and not all numbers
            if word not in word_dict:
                word_dict[word] = 1
            if word in word_dict:
                word_dict[word] +=1
    top_words= sorted(word_dict.items(), key=lambda(k,v):(v,k),reverse=True)[0:25]
    top25words = []
    for w in top_words:
        top25words.append(w[0])
    return top25words

def getTextSentiment(webtext):
        articletext = ''
        soup = BeautifulSoup(webtext)
        for tag in soup.findAll('p'): #,attrs = {"class":"story-body-text story-content"}):
            try:
                articletext += str(tag.contents[0])
            except:
                a=0
        return getsentiment.getSentiment (articletext[0:2000])