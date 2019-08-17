
# Code you have previously used to load data
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.pipeline import Pipeline

# CONSTANTS
CONDITIONS_DICT = {"NA": 0, "Po": 1, "Fa": 2, "TA": 3, "Gd":4, "Ex": 5}
CORRELATION_LEVEL = 0.025
NUMERICS = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
TRAIN_TEST_SPLIT = 0.85
EXCLUDED_LABELS = ["1stFlrSF", "1stFlrSF", "BsmtUnfSF", "TotalBsmtSF"]
CATEGORY_LABELS = {"KitchenQual":    CONDITIONS_DICT,
                    "GarageCond":    CONDITIONS_DICT,
                    "ExterQual":     CONDITIONS_DICT,
                    "ExterCond":     CONDITIONS_DICT,
                    "LotConfig":     {"Inside": 0, "Corner": 6, "CulDSac": 10, "FR2": 3, "FR3":4},
                    "Utilities":     {"ELO": 0, "NoSeWa": 1, "NoSewr": 2, "AllPub": 3},
                    "LandSlope":     {"Gtl": 10, "Mod": 4, "Sev": 1},
                    "LotShape":     {"Reg": 10, "IR1": 5, "IR2": 3, "IR3": 1},
                    }

#
def getCorrelatedFeatureNames(corr_series, tolerance, Tag):
    result = []
    for index, value in corr_series.items():
        if abs(value) > tolerance and index != Tag:
            result.append(index)

    return result

# Path of the file to read. We changed the directory structure to simplify submitting to a competition
iowa_file_path = '../data/train.csv'

home_data = pd.read_csv(iowa_file_path)

# drop columns that we dont care about
home_data = home_data.drop(EXCLUDED_LABELS, axis=1)

# replace categorical attributes with numerical ones
home_data.replace(CATEGORY_LABELS, inplace=True)

# make a copy that only contains numerics
home_data_copy = home_data.copy().select_dtypes(include=NUMERICS)


home_data_copy = home_data_copy.drop(["Id"], axis=1)
corr_matrix1 = home_data_copy.corr()
corr_series = corr_matrix1["SalePrice"].sort_values(ascending = False)
corr_features_list = getCorrelatedFeatureNames(corr_series, CORRELATION_LEVEL, "SalePrice")
print(corr_features_list)

# Create target object and call it y
y = home_data.SalePrice

# select features that are correlated
X = home_data[corr_features_list]

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, train_size = TRAIN_TEST_SPLIT, random_state=1)

# do feature scaling and normalization on training data
num_pipeline = Pipeline([
    ('imputer', Imputer(strategy="median")),
    ('std_scaler', MaxAbsScaler())])

# normalize the training data
train_X_scaled = num_pipeline.fit_transform(train_X)

# normalize test data using teh parameters learned from training data
val_X_scaled = num_pipeline.transform(val_X)

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(random_state=1, n_estimators = 300)

rf_model.fit(train_X_scaled, train_y)
rf_val_predictions = rf_model.predict(val_X_scaled)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

#now try a grid search to get optimal hyperparameters
param_grid = [{'n_estimators': [300, 500]},
              ]

grid_search = GridSearchCV(rf_model, param_grid, scoring = 'neg_mean_absolute_error', cv=5, verbose = 10)
grid_search.fit(train_X_scaled, train_y)
print(grid_search.best_params_)
print(grid_search.best_score_)

#train the best model on the full data
full_x_scaled = num_pipeline.fit_transform(X)
rf_model_full = grid_search.best_estimator_
rf_model_full.fit(full_x_scaled, y)


#path to file you will use for predictions
test_data_path = '../data/test.csv'
test_data = pd.read_csv(test_data_path)

test_data = test_data.drop(EXCLUDED_LABELS, axis=1)

# replace categorical attributes with numerical ones
test_data.replace(CATEGORY_LABELS, inplace=True)
#get numeric columns & normalize data
test_X = test_data[corr_features_list]
test_X_scaled = num_pipeline.transform(test_X)

#make predictions which we will submit. 
test_preds = rf_model_full.predict(test_X_scaled)

#The lines below shows how to save predictions in format used for competition scoring

output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('../data/submission.csv', index=False)