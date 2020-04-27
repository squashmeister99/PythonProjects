# python module that contains helper methods for ML and visualization
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import (cross_val_score, KFold)
from scipy import stats
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

def calculateWeights(myArray):
    weights = []
    sum = 2.0*np.sum(myArray)
    for item in myArray:
        val = 0.5 - float(item/sum)
        weights.append(val)

    return weights/np.sum(weights)

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
    return displayScores(-scores)
    
def displayScores(scores):
    rsme = np.sqrt(scores)
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("standard deviation:", scores.std())
    print("rsme score: {:.4f} ({:.4f})\n".format(rsme.mean(), rsme.std()))
    return rsme.mean()
    
# plot correlations
def plotCoorelations(df, annotate=True):
    correlation = df.corr()
    f, ax = plt.subplots(figsize=(14,12))
    plt.title('Correlation of numerical attributes', size=16)
    sns.heatmap(correlation, annotate)
    plt.show()
    
def reduce_mem_usage(df):
    start_mem_usg = df.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in. 
    for col in df.columns:
        if df[col].dtype != object:  # Exclude strings

            # Print current column type
            print("******************************")
            print("Column: ",col)
            print("dtype before: ",df[col].dtype)

            # make variables for Int, max and min
            IsInt = False
            mx = df[col].max()
            mn = df[col].min()

            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(df[col]).all(): 
                NAlist.append(col)
                df[col].fillna(mn-1,inplace=True)  

            # test if column can be converted to an integer
            asint = df[col].fillna(0).astype(np.int64)
            result = (df[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True


            # Make Integer/unsigned Integer datatypes
            if IsInt:
                info = np.iinfo
                # Make Integer/unsigned Integer datatypes
                if mn >= 0:
                    types = (np.uint8, np.uint16, np.uint32, np.uint64)
                else:
                    types = (np.int8, np.int16, np.int32, np.int64)
            else:
                info = np.finfo
                types = (np.float16, np.float32, np.float64)

            for t in types:
                if info(t).min <= mn and mx <= info(t).max:
                df[col] = df[col].astype(t)
                break

            # Print new column type
            print("dtype after: ",df[col].dtype)
            print("******************************")

    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = df.memory_usage().sum() / 1024**2 
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return df, NAlist
