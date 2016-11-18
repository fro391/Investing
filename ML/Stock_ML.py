def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation, neighbors, svm
from sklearn.linear_model import LinearRegression

if __name__ == '__main__':

    #Learning data
    df = pd.read_csv('C:\\Users\\Richard\\Desktop\\Python\\Investing\\YQL\\data\\VPNoutput.csv')
    df.replace('NaN',0,inplace = True)
    df.drop(['Ticker&Date'],1,inplace = True)

    X = np.array(df.drop(['FutP'],1))
    X = preprocessing.scale(X)
    y = np.array(df['FutP'])

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size= 0.1)

    #Model training
    clf = LinearRegression()
    clf.fit(X, y)

    #New data
    df = pd.read_csv('C:\\Users\\Richard\\Desktop\\Python\\Investing\\YQL\\data\\VPNoutput2016-11-18.csv')
    df = df.drop(df[df.EPS < 0].index) #removes stocks with EPS<0
    df.replace('NaN',0,inplace = True)

    X_test = np.array(df)

    Output = {}

    #Output
    for i in X_test:
        try:
            k = np.delete(i,0)
            prediction = clf.predict(k)
            Output[str(i[0][:-8])] = float(prediction)
        except:
            pass

    Output = sorted(Output, key=Output.get, reverse=True) #sort from highest to smallest
    print Output