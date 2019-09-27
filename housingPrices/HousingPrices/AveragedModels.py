from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split
import numpy as np

class AveragingModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, models):
        self.models_ = models
        print(self.models_)
        
    # define clones of the original models to fit the data in
    def fit(self, X, y):
        self.models_ = [clone(x) for x in self.models_]
        
        # Train cloned base models
        for model in self.models_:
            model.fit(X, y)

        return self
    
    #do the predictions for cloned models and average them
    def predict(self, X):
        print(self.models_)
        predictions = np.column_stack([
            model.predict(X) for model in self.models_
        ])
        return np.mean(predictions, axis=1)   


