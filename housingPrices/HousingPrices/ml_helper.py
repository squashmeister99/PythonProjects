# python module that contains helper methods for ML and visualization
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import (cross_val_score, KFold)
from scipy import stats
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns


def outlierDetect_IsolationForest(df, contaminationLevel = 0.02):
    df_numeric = df.select_dtypes(exclude=object) 
    imp_mean = SimpleImputer()
    df_numeric_t = imp_mean.fit_transform(df_numeric)
    clf = IsolationForest(contaminationLevel)
    preds = clf.fit_predict(df_numeric_t)
    outliers = np.where(preds == -1)
    df_out = df.drop(labels = outliers[0], inplace=False, errors = "ignore")
    print("number of outliers = {0}".format(len(outliers[0])))
    return df_out, outliers

# outlierDetect_ZScore
def outlierDetect_ZScore(df, zValue = 3):
    df_numeric = df.select_dtypes(exclude=object)    
    z = np.abs(stats.zscore(df_numeric))
    outliers = np.where(z > zValue)
    # drop outliers 
    df_out = df.drop(labels = outliers[0], inplace=False, errors = "ignore")

    print("number of outliers = {0}".format(len(outliers[0])))
    return df_out, outliers

def columnsWithMissingData(X, threshold = 0.9):
    # check for null items
    null_df = X.columns[X.isnull().any()]
    null_count = X[null_df].isnull().sum()/len(X.index)
    null_count_above_threshold = null_count.loc[null_count > threshold]
    null_count_above_threshold
    
    #percentage of zero values for each numeric variable
    zero_df = X.columns[(X == 0).any()]
    zero_count = (X[zero_df] == 0).sum()/len(X.index)
    zero_count_above_threshold = zero_count.loc[zero_count > threshold]
    return pd.concat([null_count_above_threshold, zero_count_above_threshold])
    
def scatterPlot(df, X, Y, font=13):
    fig, ax = plt.subplots()
    ax.scatter(x = df[X], y = df[Y])
    plt.ylabel(Y, fontsize=13)
    plt.xlabel(X, fontsize=13)
    plt.show()
    
def crossValidateModel(model, X, y, name="<unknown>", threads = -1):
    start = time.time()
    kf = KFold(5, shuffle=True, random_state=42).get_n_splits(X)
    scores = cross_val_score(model, X, y, scoring = "neg_mean_absolute_error", n_jobs = threads, verbose = 4, cv = kf)
    end = time.time()
    elapsed_time = end - start
    print("model {0} cross_val_score took {1} seconds".format(name, elapsed_time))
    displayScores(-scores)
    
def displayScores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("standard deviation:", scores.std())
    
# plot correlations
def plotCoorelations(df, annotate=True):
    correlation = df.corr()
    f, ax = plt.subplots(figsize=(14,12))
    plt.title('Correlation of numerical attributes', size=16)
    sns.heatmap(correlation, annotate)
    plt.show()