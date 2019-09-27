# python module that contains helper methods for ML and visualization
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

def outlierDetect_IsolationForest(df, contaminationLevel = 0.02):
    df_numeric = df.select_dtypes(exclude=object) 
    imp_mean = SimpleImputer()
    df_numeric_t = imp_mean.fit_transform(df_numeric)
    clf = IsolationForest( behaviour = 'new', contaminationLevel)
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
    return home_data_out, outliers

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

def plotHeatmap(df):
    corrmat = df.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, vmax=.8, square=True)
    plt.show()