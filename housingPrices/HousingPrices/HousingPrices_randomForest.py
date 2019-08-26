import pandas as pd
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (StandardScaler, MinMaxScaler, PowerTransformer, RobustScaler)
from sklearn.pipeline import Pipeline
from scipy import stats
import numpy as np

# CONSTANTS
CONDITIONS_DICT = {"NA": 0, "NaN": 0, "nan": 0, "Po": 2, "Fa": 3, "TA": 4, "Gd":6, "Ex": 10}
CORRELATION_LEVEL = 0.0
NUMERICS = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
TRAIN_TEST_SPLIT = 0.85
EXCLUDED_LABELS = ["1stFlrSF", "1stFlrSF", "BsmtUnfSF", "TotalBsmtSF"]
CATEGORY_LABELS = {"KitchenQual":       CONDITIONS_DICT,
                    "GarageCond":       CONDITIONS_DICT,
                    "GarageQual":       CONDITIONS_DICT,
                    "ExterQual":        CONDITIONS_DICT,
                    "ExterCond":        CONDITIONS_DICT,
                    "BsmtQual":         CONDITIONS_DICT,
                    "BsmtCond":         CONDITIONS_DICT,
                    "FireplaceQu" :     CONDITIONS_DICT,
                    "HeatingQC" :     CONDITIONS_DICT,
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

# pipeline to do feature scaling and normalization on training data
PIPELINE = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler())])

#
def getCorrelatedFeatureNames(corr_series, tolerance, Tag):
    result = []
    for index, value in corr_series.items():
        if abs(value) > tolerance and index != Tag:
            result.append(index)

    return result

# load housing data
iowa_file_path = '../data/train.csv'
home_data = pd.read_csv(iowa_file_path)

# drop columns that we dont care about
#home_data = home_data.drop(EXCLUDED_LABELS, axis=1)

# replace categorical attributes with numerical ones
home_data.replace(CATEGORY_LABELS, inplace=True)
home_data[["BsmtCond", "MiscFeature", "GarageQual", "GarageType"]].fillna(0, inplace=True)

# make a copy that only contains numerics
home_data_copy = home_data.copy().select_dtypes(include=NUMERICS)
copy2 = home_data.select_dtypes(exclude=NUMERICS)
#print(home_data["GarageType"].unique())
#print(copy2["GarageFinish"].unique())

home_data_copy = home_data_copy.drop(["Id"], axis=1)
# try coorelation after transform
corr_matrix1 = home_data_copy.corr()
corr_series = corr_matrix1["SalePrice"].sort_values(ascending = False)

corr_features_list = getCorrelatedFeatureNames(corr_series, CORRELATION_LEVEL, "SalePrice")
#print(corr_features_list)

# Create target object and call it y
y = home_data.SalePrice

# select features that are correlated. this selects a subset of columns from the original dataset
X = home_data[corr_features_list]
print(X.dtypes)

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, train_size = TRAIN_TEST_SPLIT, random_state=1)

# normalize the training data
train_X_scaled = PIPELINE.fit_transform(train_X)

# try a few scatterplots to see data distrubution

# normalize test data using teh parameters learned from training data
val_X_scaled = PIPELINE.transform(val_X)

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(random_state=1, n_estimators = 500)

rf_model.fit(train_X_scaled, np.log(train_y))
rf_val_predictions = rf_model.predict(val_X_scaled)
rf_val_mae = mean_absolute_error(np.exp(rf_val_predictions), val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

##now try a grid search to get optimal hyperparameters
param_grid = [{'n_estimators': [300, 500, 600]}]
grid_search = GridSearchCV(rf_model, param_grid, cv=5, verbose = 10)
grid_search.fit(train_X_scaled, np.log(train_y))
print(grid_search.best_params_)
print(grid_search.best_score_)

#train the best model on the full data
full_x_scaled = PIPELINE.fit_transform(X)
rf_model_full = grid_search.best_estimator_
rf_model_full.fit(full_x_scaled, np.log(y))

#path to file you will use for predictions
test_data_path = '../data/test.csv'
test_data = pd.read_csv(test_data_path)

#test_data = test_data.drop(EXCLUDED_LABELS, axis=1)

# replace categorical attributes with numerical ones
# extract and scale the necessary test data
test_data.replace(CATEGORY_LABELS, inplace=True)
#get numeric columns & normalize data
test_X = test_data[corr_features_list]
test_X_scaled = PIPELINE.transform(test_X)

#make predictions which we will submit. 
log_test_preds = rf_model_full.predict(test_X_scaled)
test_preds = np.exp(log_test_preds)

#The lines below shows how to save predictions in format used for competition scoring
output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('../data/submission.csv', index=False)