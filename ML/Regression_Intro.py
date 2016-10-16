import pandas as pd
import quandl,math, datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import urllib
import pickle

style.use('ggplot')

#df = quandl.get('WIKI/GOOG')

#get stock info into pandas df
'''urllib.urlretrieve('http://real-chart.finance.yahoo.com/table.csv?s=BRK-A&a=03&b=12&c=1996&d=08&e=28&f=2016&g=d&ignore=.csv',
                    'BRK-A.csv')'''
df = pd.read_csv('BRK-A.csv',index_col=0)

#make HL pct and pct change columns and select necessary columns
df = df [['Open','High','Low','Adj Close','Volume']]
df ['HL_PCT'] = (df['High'] - df['Adj Close'])/df['Adj Close'] * 100.0
df ['PCT_change'] = (df['Adj Close'] - df['Open'])/df['Open'] * 100.0
df = df[['Adj Close','HL_PCT','PCT_change','Volume']]

forecast_col = 'Adj Close'
df.fillna(-99999,inplace = True)

forecast_out = int(math.ceil(0.01*len(df))) #days to forecast out
df['label'] = df[forecast_col].shift(-forecast_out) #shifting so that forecast_col will have future data

x = np.array(df.drop(['label'],1))
x = preprocessing.scale(x)
x = x[:-forecast_out]
x_lately = x[-forecast_out:]

df.dropna(inplace=True)
y = np.array(df['label'])

x_train,x_test,y_train, y_test = cross_validation.train_test_split(x,y,test_size = 0.2)

'''clf = LinearRegression()
clf.fit(x_train,y_train)
#pickling classifier
with open('LinearR.pickle','wb') as f:
    pickle.dump(clf,f)'''

pickle_in = open('LinearR.pickle','rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(x_test,y_test)
forecast_set = clf.predict(x_lately)
print forecast_set,accuracy,forecast_out