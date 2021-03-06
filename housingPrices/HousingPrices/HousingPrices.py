
# Code you have previously used to load data
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Path of the file to read. We changed the directory structure to simplify submitting to a competition
iowa_file_path = '../data/train.csv'

home_data = pd.read_csv(iowa_file_path)

# Create target object and call it y
y = home_data.SalePrice


# drop the Id column and sales price column
home_data = home_data.drop("Id", axis=1)
home_data = home_data.drop("SalePrice", axis=1)
print(home_data.info())

# get info on colums that have numeric types
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

X = home_data.select_dtypes(include=numerics)

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, train_size = 0.85, random_state=1)
# do feature scaling and normalization on training data
num_pipeline = Pipeline([
    ('imputer', Imputer(strategy="median")),
    ('std_scaler', StandardScaler())])

# normalize the training data
train_X_scaled = num_pipeline.fit_transform(train_X)

# normalize test data using teh parameters learned from training data
val_X_scaled = num_pipeline.transform(val_X)

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(random_state=1, n_estimators=300)

rf_model.fit(train_X_scaled, train_y)
rf_val_predictions = rf_model.predict(val_X_scaled)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

# now try a grid search to get optimal hyperparameters
param_grid = [{'n_estimators': [ 300, 500]},
              ]

grid_search = GridSearchCV(rf_model, param_grid, scoring = 'neg_mean_absolute_error', cv=5)
grid_search.fit(train_X_scaled, train_y)
print(grid_search.best_params_)
print(grid_search.best_score_)

# train the best model on the full data
full_x_scaled = num_pipeline.fit_transform(X)
rf_model_full = RandomForestRegressor(random_state=1, n_estimators=500)
rf_model_full.fit(full_x_scaled, y)


# path to file you will use for predictions
test_data_path = '../data/test.csv'

test_data = pd.read_csv(test_data_path)
# drop the Id column
test_data2 = test_data.drop("Id", axis=1)

# get numeric columns & normalize data
test_X = test_data2.select_dtypes(include=numerics)
test_X_scaled = num_pipeline.transform(test_X)

# make predictions which we will submit. 
test_preds = rf_model_full.predict(test_X_scaled)

# The lines below shows how to save predictions in format used for competition scoring

output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('../data/submission.csv', index=False)