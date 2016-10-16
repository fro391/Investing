from __future__ import division
import urllib
import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import cPickle as pickle
import matplotlib.pyplot as plt
import warnings
from matplotlib import style
from collections import Counter
import pandas as pd
import random


def k_n_n (data,predict,k=3):
    if len(data)>=k:
        warnings.warn('K is set to a value less than total voting groups!')
    distances = []
    for group in data:
        for features in data[group]:
            e_d = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([e_d,group])

    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]

    return vote_result

if __name__ == '__main__':
    df = pd.read_csv('breast_cancer_data.csv')
    df.replace('?',-99999, inplace = True)
    df.drop(['id'],1,inplace = True)
    full_data = df.astype(float).values.tolist()

    random.shuffle(full_data)

    test_size = 0.2
    train_set = {2:[],4:[]}
    test_set = {2:[],4:[]}
    train_data = full_data[:-int(test_size*len(full_data))]
    test_data = full_data[-int(test_size*len(full_data)):]

    for i in train_data:
        train_set[i[-1]].append(i[:-1])

    for i in test_data:
        test_set[i[-1]].append(i[:-1])

    correct = 0
    total = 0

    for group in test_set:
        for data in test_set[group]:
            vote = k_n_n(train_set,data,k=5)
            if group == vote:
                correct += 1
            total += 1

    print 'Accuracy: ', float(correct/total)