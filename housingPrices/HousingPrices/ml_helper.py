# python module that contains helper methods for ML and visualization
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# plot correlations
def plotCoorelations(df):
    # remove non_numeric features  
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm').set_precision(2)
    
def plotHeatmap(df):
    corrmat = df.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, vmax=.8, square=True)
    plt.show()

# define a method to use Isolation Forest for outlier detection
def outlierRemoval_IsolationForest(X, y, outlierFraction = 0.02):
    clf = IsolationForest( behaviour = 'new', contamination = outlierFraction)
    preds = clf.fit_predict(X)
    outliers = np.where(preds == -1)
    return dropOutliers(X, y, outliers)

def dropOutliers(X, y, outliers):
    print("number of outliers = {0}".format(len(outliers[0])))
    # drop outliers
    X_clean = np.delete(X, outliers[0], axis = 0)
    y_clean = np.delete(y.values, outliers[0])
    return X_clean, y_clean, outliers[0] 

# define a method to use Isolation Forest for outlier detection
def outlierRemoval_ZScore(X, y, zValue = 3, bypass=False):
    if bypass:
        return X, y, []
    z = np.abs(stats.zscore(X))
    outliers = np.where(z > zValue)
    return dropOutliers(X, y, outliers)

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

