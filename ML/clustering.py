import pandas as pd
import urllib
import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
import cPickle as pickle

if __name__ == '__main__':

    '''urllib.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',
                        'breast_cancer_data.csv')'''

    df = pd.read_csv('breast_cancer_data.csv')
    df.replace('?',-99999,inplace = True)
    df.drop(['id'],1,inplace = True)

    X= np.array(df.drop(['class'],1))
    y= np.array(df['class'])

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size= 0.2)

    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)
    with open('KNeighb.p','wb') as f:
        pickle.dump(clf,f)

    clf = pickle.load(open('KNeighb.p','rb'))

    accuracy = clf.score(X_test,y_test)
    print accuracy

    example_measures = np.array([[10,2,4,1,5,2,3,2,1],[1,2,4,1,5,2,3,2,1]])
    example_measures = example_measures.reshape(len(example_measures),-1)

    prediction = clf.predict(example_measures)
    print prediction