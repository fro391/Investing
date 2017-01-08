def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation
from sklearn.linear_model import LinearRegression, LogisticRegression, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor, RandomForestRegressor
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
import glob, os
import cPickle as pk
import datetime
import smtplib
from email.mime.text import MIMEText

def ML (dir,file,emailAddress,password):
    msg = ''
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

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size= 0.2)

    #Model 1 training
    clf = AdaBoostRegressor()
    clf.fit(X_train, y_train.astype(int)) #change float lable to int
    msg += 'Ada boosting score is: %s \n' % str(clf.score(X_test,y_test.astype(int))) #change float lable to int
    clf.fit(X, y.astype(int)) #change float lable to int
    #save Model
    with open('stocksA.p','wb') as f:
        pk.dump(clf,f)
    clf = pk.load(open('stocksA.p','rb'))

    #Model 2 training
    clf2 = GradientBoostingRegressor()
    clf2.fit(X_train, y_train.astype(int)) #change float lable to int
    msg += 'Gradient boosting score is: %s \n' % str(clf2.score(X_test,y_test.astype(int))) #change float lable to int
    clf2.fit(X, y.astype(int)) #change float lable to int
    #save Model
    with open('stocksB.p','wb') as f:
        pk.dump(clf2,f)
    with open ('stocksB.p','rb') as f:
        clf2 = pk.load(f)

    #New data
    df = pd.read_csv(dir + file)
    df = df.drop(df[df.EPS < 0].index) #removes stocks with EPS<0

    X_predict = np.array(df)

    Output = {}
    #Output 1
    for i in X_predict:
        try:
            k = np.delete(i,0)
            prediction = clf.predict(k)
            Output[str(i[0][:-8])] = float(prediction)
        except:
            pass

    D_New = {k: v for k, v in Output.items() if v>0}#remove negative price increase predictions
    msg += (str(len(D_New))+ '\n')
    #msg += (str(D_New)+'\n')
    D_New = sorted(D_New, key=D_New.get, reverse=True) #sort from highest to smallest
    msg += (str(D_New) + '\n')

    Output2 = {}
    #Output 2
    for i in X_predict:
        try:
            k = np.delete(i,0)
            prediction = clf2.predict(k)
            Output2[str(i[0][:-8])] = float(prediction)
        except:
            pass

    D_New2 = {k: v for k, v in Output2.items() if v>0}#remove negative price increase predictions
    msg += (str(len(D_New2)) + '\n')
    #msg += (str(D_New2) + '\n')
    D_New2 = sorted(D_New2, key=D_New2.get, reverse=True) #sort from highest to smallest
    msg += (str(D_New2) + '\n')


    #send results to email
    msg = MIMEText(msg)
    msg ['Subject'] = '%s stock analysis' % str(datetime.datetime.today().strftime('%Y-%m-%d'))
    msg ['From'] = emailAddress
    msg ['To'] = emailAddress
    try:
        s = smtplib.SMTP('smtp-mail.outlook.com',25)
        s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
        s.starttls() #Puts connection to SMTP server in TLS mode
        s.ehlo()
        s.login(emailAddress, password)
        s.sendmail(emailAddress,emailAddress,msg.as_string())
        s.quit()
        print 'email sent to: %s' %emailAddress
    except:
        raise

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
            '''learning_df.set_index('Ticker&Date').to_csv(data_dir +'LearningFile.csv')''' #used to generate learning file if accidentally deleted
            #appending learning file to master learning file
            VPNOutput = pd.read_csv(data_dir +'LearningFile.csv')
            outputF =  VPNOutput.append(learning_df).drop_duplicates().set_index('Ticker&Date')
            outputF.to_csv(data_dir +'LearningFile.csv')

    #retriev password
    with open('C:\\Users\\Richard\\Desktop\\Python\\hotmail.txt', 'rb') as f:
        email_list = f.read().split(',')

    ML(data_dir,file_list[0],email_list[0],email_list[1])