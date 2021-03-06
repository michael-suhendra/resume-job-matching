# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:05:38 2019

@author: User
"""

# prerequisites
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download()

import pandas as pd
import numpy as np
import os
import csv

def read_file(folder, file):
    """
    Helper method that reads a .txt file and returns the text body
    Args:
        folder: path to directory
        file: filename
    Returns:
        data: content of the file as string
    """
    
    data = ''
    if os.path.isfile(os.path.join(folder, file + '.txt')):
        filename = os.path.join(folder, file)
        with open(filename + '.txt', 'r', encoding='utf8') as file:
            data = file.read().replace('\n', ' ')
    return data
    
def generate_data_for_resume_matcher(filename):
    """
    Create array with .csv file for mapping as input
    Args:
        filename: name of the .csv file
    Returns:
        pairs: numpy array of cv/jobpost pairs
        labels: numpy array of labels
    """
    cv = []
    jobpost = []
    labels = []
    
    with open(filename, 'rt') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            cv_text = read_file('cv/', row[0])
            jobpost_text = read_file('jobpost/', row[1])
            
            cv.append(cv_text)
            jobpost.append(jobpost_text)
            labels.append(int(row[2]))
    
    df = pd.DataFrame({'cv': cv,
                       'jobpost': jobpost,
                       'labels': labels})
    
    # attempt to balance classes
    #labels = df.groupby('labels')
    # Sort the over-represented class to the head.
    #labels = labels[labels.apply(len).sort_values(ascending=False).index]
    #excess = len(labels.iloc[0]) - len(labels.iloc[1])
    #remove = np.random.choice(labels.iloc[0], excess, replace=False)
    #df = df[~df.name.isin(remove)]
    # downsample majority class (in this case class 5)
    df_not_majority = df[df['labels'] != 5]
    df_majority = df[df['labels'] == 5]
    
    df_majority = df_majority.sample(210)
    df = pd.concat([df_not_majority, df_majority], axis=0)
    
    df_not_majority = df[df['labels'] != 4]
    df_majority = df[df['labels'] == 4]
    
    df_majority = df_majority.sample(210)
    df = pd.concat([df_not_majority, df_majority], axis=0)
    
    df_not_majority = df[df['labels'] != 3]
    df_majority = df[df['labels'] == 3]
    
    df_majority = df_majority.sample(210)
    df = pd.concat([df_not_majority, df_majority], axis=0)
    
    df_not_majority = df[df['labels'] != 2]
    df_majority = df[df['labels'] == 2]
    print(df_majority)
    
    df_majority = df_majority.sample(210)
    df = pd.concat([df_not_majority, df_majority], axis=0)
    
    df_not_majority = df[df['labels'] != 1]
    df_majority = df[df['labels'] == 1]
    
    df_majority = df_majority.sample(210)
    df = pd.concat([df_not_majority, df_majority], axis=0)
    
    # plot number of instances of each class
    df['labels'].value_counts().plot(kind='bar', title='Count (target)')
    
    # convert to numpy array
    
    df_pairs = df[['cv', 'jobpost']]
    df_labels = df['labels']
    
    pairs = df_pairs.to_numpy()
    labels = df_labels.to_numpy()
    
    return pairs, labels

def generate_data_for_sts():
    """
    Create array with .csv file for mapping as input
    Args:
        filename: name of the .csv file
    Returns:
        sts_train: dataframe of training set
        sts_test: dataframe of test set
    """
    STS_COLUMNS = ['label','s1','s2']

    # read data
    sts_train = pd.read_csv('data/sts-train.csv',sep='\t',usecols=[i for i in range(4,7)],names=STS_COLUMNS)
    sts_test = pd.read_csv('data/sts-test.csv',sep='\t',usecols=[i for i in range(4,7)],quoting=csv.QUOTE_NONE,names=STS_COLUMNS)
    
    # drop rows with nan values
    sts_train = sts_train.dropna(axis=0,how='any')
    sts_test = sts_test.dropna(axis=0,how='any')
    
    return sts_train, sts_test
