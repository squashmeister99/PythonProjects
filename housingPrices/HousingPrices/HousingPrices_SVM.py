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

# Data Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# plot correlations
def plotCoorelations(df):
    # remove non_numeric features  
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm').set_precision(2)

# define a method to use Isolation Forest for outlier detection
def outlierDetect_IsolationForest(home_data):
    clf = IsolationForest( behaviour = 'new', contamination= 0.02)
    preds = clf.fit_predict(home_data)
    outliers = np.where(preds == -1)

    # drop outliers from home data
    home_data_out = np.delete(home_data.todense(), outliers[0], axis = 0)
    print("number of outliers = {0}".format(len(outliers[0])))

    return home_data_out, outliers


# define a method to use Isolation Forest for outlier detection
def outlierDetect_ZScore(home_data, zValue = 3):
    X_numeric = home_data.select_dtypes(exclude=object) 
    
    z = np.abs(stats.zscore(X_numeric))
    outliers = np.where(z > zValue)

    # drop outliers from home data
    home_data_out = home_data.drop(labels = outliers[0], inplace=False, errors = "ignore")
    #home_data_out = home_data[(preds == -1).all(axis=1)]
    print("number of outliers = {0}".format(len(outliers[0])))
    return home_data_out, outliers


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

cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

transformers=[
        ('log', log_pipeline, log_features_names),
        ('num', numeric_pipeline, numeric_features_names),
        ('cat', cat_pipeline, categorical_features_names),
        ('year', year_pipeline, year_features_names)     
    ]

ct = ColumnTransformer(transformers=transformers)
Xt = ct.fit_transform(X_train)

# perform mean normalization and feature scaling on the data
print(y_train.iloc[766])
X_train_t, outliers = outlierDetect_IsolationForest(Xt)
y_train = np.delete(y_train.values, outliers[0])

clf = RandomForestRegressor(random_state=1, n_estimators = 300, criterion="mae")

# fit the log of the sale price
clf.fit(X_train_t, np.log1p(y_train))

y_predict = clf.predict(ct.transform(X_test))

rf_val_mae = mean_absolute_error(y_test, np.expm1(y_predict))

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))


