def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation
from sklearn.linear_model import LinearRegression, LogisticRegression, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
import glob, os
import cPickle as pk

def ML (dir,file):
    #Learning data
    df = pd.read_csv(dir + 'LearningFile.csv')
    df.replace('NaN',0,inplace = True)#Remove null
    df.replace('#N/A',0,inplace = True)#Remove null
    df.replace('inf',0,inplace=True)#Remove infinity
    df.drop(['Ticker&Date'],1,inplace = True)

    X = np.array(df.drop(['priceChange_y'],1))
    X = preprocessing.scale(X)
    df['priceChange_y'] = df['priceChange_y'].map(lambda x: x * 100) #multiply float to make percentage
    y = np.array(df['priceChange_y'])
    y = preprocessing.scale(y)

    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size= 0.2)

    #Model training
    clf = BayesianRidge()
    clf.fit(X, y.astype(int)) #change float lable to int
    #save Model
    with open('stocks.p','wb') as f:
        pk.dump(clf,f)
    clf = pk.load(open('stocks.p','rb'))

    #print clf.score(X_test,y_test.astype(int)) #change float lable to int

    #New data
    df = pd.read_csv(dir + file)
    df = df.drop(df[df.EPS < 0].index) #removes stocks with EPS<0
    df.replace('NaN',0,inplace = True)

    X_predict = np.array(df)

    Output = {}

    #Output
    for i in X_predict:
        try:
            k = np.delete(i,0)
            prediction = clf.predict(k)
            Output[str(i[0][:-8])] = float(prediction)
        except:
            pass

    D_New = {k: v for k, v in Output.items() if v>0}#remove negative price increase predictions
    print len(D_New)
    print D_New
    D_New = sorted(D_New, key=D_New.get, reverse=True) #sort from highest to smallest
    print D_New

if __name__ == '__main__':

    data_dir = 'C:\\Users\\Richard\\Desktop\\Python\\Investing\\YQL\\data\\'
    file_list = []
    os.chdir(data_dir)
    for file in glob.glob("*.csv"):
        file_list.append(file)
    file_list =  sorted(file_list,reverse = True)

    for i in range(len(file_list)-3): #iterate through all available VPN files
        if int(file_list[i][-6:-4]) - int(file_list[i+1][-6:-4]) in (1,3): #Vlooking up today's price change to yesterday's price change
            df_today = pd.read_csv(data_dir + '%s' %file_list[i])[['Ticker&Date','priceChange']]
            df_today['Ticker&Date'] = df_today['Ticker&Date'].map(lambda x: x.lstrip('+-').rstrip('0123456789'))
            df_yes = pd.read_csv(data_dir + '%s' %file_list[i+1])
            df_yes['Ticker&Date'] = df_yes['Ticker&Date'].map(lambda x: x.lstrip('+-').rstrip('0123456789'))
            learning_df =  df_yes.merge(df_today, on = 'Ticker&Date', how = 'left')
            learning_df['Ticker&Date'] = learning_df['Ticker&Date'] + file_list[i][-14:-4].replace('-','') #adding back timestamp
            '''learning_df.set_index('Ticker&Date').to_csv(data_dir +'LearningFile.csv')'''
            #appending learning file to master learning file
            VPNOutput = pd.read_csv(data_dir +'LearningFile.csv')
            outputF =  VPNOutput.append(learning_df).drop_duplicates().set_index('Ticker&Date')
            outputF.to_csv(data_dir +'LearningFile.csv')

    ML(data_dir,file_list[0])