from sklearn.ensemble import (RandomForestRegressor, IsolationForest)
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import (train_test_split, GridSearchCV)
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (StandardScaler, OneHotEncoder, FunctionTransformer, KBinsDiscretizer)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from scipy import stats
import numpy as np
import pandas as pd
import time

# Data Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

CONDITIONS_DICT = {"NA": 0, "NaN": 0, "nan": 0, "Po": 2, "Fa": 3, "TA": 4, "Gd":6, "Ex": 10}

# constants
CATEGORY_LABELS = {"KitchenQual":       CONDITIONS_DICT,
                    "GarageCond":       CONDITIONS_DICT,
                    "GarageQual":       CONDITIONS_DICT,
                    "ExterQual":        CONDITIONS_DICT,
                    "ExterCond":        CONDITIONS_DICT,
                    "BsmtQual":         CONDITIONS_DICT,
                    "BsmtCond":         CONDITIONS_DICT,
                    "FireplaceQu" :     CONDITIONS_DICT,
                    "HeatingQC" :       CONDITIONS_DICT,
                    "LotConfig":     {"Inside": 0, "Corner": 6, "CulDSac": 10, "FR2": 3, "FR3":4},
                    "Utilities":     {"ELO": 0, "NoSeWa": 1, "NoSewr": 2, "AllPub": 3},
                    "LandSlope":     {"Gtl": 10, "Mod": 4, "Sev": 1},
                    "LotShape":     {"Reg": 10, "IR1": 5, "IR2": 3, "IR3": 1},
                    "GarageType":     {"NA": 0, "nan": 0, "Basment": 4,  "Detchd": 1, "CarPort": 3, "BuiltIn": 5, "Attchd": 7, "2Types": 12},
                    "BldgType":     {"TwnhsI": 1, "Twnhs": 2, "TwnhsE": 3, "Duplex": 5,  "2fmCon": 7, "1Fam": 12},
                    "CentralAir":     {"N": 1, "Y": 10},
                    "Electrical":     {"Mix": 1, "FuseP": 3, "FuseF": 5,  "FuseA": 7, "SBrkr": 12},
                    "MSZoning":     {"RL": 100, "RM": 60, "C (all)": 20, "FV": 30, "RH": 30},
                    "LandContour":     {"Lvl": 100, "Low": 15, "Bnk": 25, "HLS": 5},
                    "Fence":     {"NA": 0, "MnPrv": 25, "MnWw": 15, "GdWo": 40, 'GdPrv': 100},
                    "Functional":     {"Typ": 100, "Min1": 70, "Min2": 50, "Mod": 40, "Maj1": 25, "Maj2": 20, "Min2": 10, "Sev": 5, "Sal": 1},
                    "MiscFeature":     {"NA": 0, "Shed": 30, "Gar2": 40, "Othr": 25, "TenC": 100},
                    "PavedDrive":     {"Y": 100, "P": 30, "N": 0},
                    }

CAT_COLS_TO_IGNORE = ["Functional",
                        "MiscFeature",
                        "Electrical",
                        "Fence",
                        "FireplaceQu",
                        "HeatingQC",
                        "GarageType"
                    ]

CAT_COLS = [ x for x in CATEGORY_LABELS.keys() if x not in CAT_COLS_TO_IGNORE]
print(CAT_COLS)

# plot correlations
def plotCoorelations(df):
    # remove non_numeric features  
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm').set_precision(2)

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
    return X_clean, y_clean 

# define a method to use Isolation Forest for outlier detection
def outlierRemoval_ZScore(X, y, zValue = 3):
    X_numeric = X.select_dtypes(exclude=object)   
    z = np.abs(stats.zscore(X_numeric))
    outliers = np.where(z > zValue)
    return dropOutliers(X, y, outliers)

def getTransformedColumnNames(ct):
    for item in ct.named_transformers_:
       pipeline = ct.named_transformers_[item]
       for step in pipeline.named_steps:
           t1 = pipeline.named_steps[step]
           print(t1.get_feature_names())

   
# load housing data
iowa_file_path = '../data/train.csv'
home_data = pd.read_csv(iowa_file_path)
Y = home_data["SalePrice"]
X = home_data.drop(columns = ["Id", "SalePrice"])

# split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=1)
print(X_train.shape)

# perform feature scaling

numeric_features = X_train.select_dtypes(exclude=object) 
num_features_names = numeric_features.columns

# features that need a log transformation
log_features_names = ["LotFrontage", "LotArea", "1stFlrSF", "GrLivArea", "OpenPorchSF"]

log_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('logscaler', FunctionTransformer(np.log1p, validate=False)),
    ('scaler', StandardScaler())])

#kbinDiscretizer features
year_features_names = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold']
year_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('kbd', KBinsDiscretizer(n_bins=5, encode='onehot-dense'))])

#numeric features that require a normal transformation
numeric_features_names = [x for x in num_features_names if x not in log_features_names + year_features_names]
print(len(numeric_features_names))

numeric_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

#categorical features
categorical_features_names = X_train.select_dtypes(include=object).columns
#categorical_features_names = CAT_COLS

cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

transformers=[
        ('log', log_pipeline, log_features_names),
        ('num', numeric_pipeline, numeric_features_names),
        ('cat', cat_pipeline, categorical_features_names),
        ('year', year_pipeline, year_features_names)     
    ]

# ensure that result is always a dense matrix
ct = ColumnTransformer(transformers=transformers, sparse_threshold = 0)

Xt = ct.fit_transform(X_train)

# perform mean normalization and feature scaling on the data
X_train_t, y_train = outlierRemoval_IsolationForest(Xt, y_train)
print(X_train_t.shape)

clf = RandomForestRegressor(random_state=1, n_estimators = 300, criterion="mae", n_jobs=-1)

# fit the log of the sale price
start = time.time()
clf.fit(X_train_t, np.log1p(y_train))
end = time.time()
elapsed_time = end - start
print("fit took {0} seconds".format(elapsed_time))

y_predict = clf.predict(ct.transform(X_test))

rf_val_mae = mean_absolute_error(y_test, np.expm1(y_predict))
print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))


