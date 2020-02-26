#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        try:
            return X[self.columns]
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError("The DataFrame does not include the columns: %s" % cols_error)
            
class TransportAggregate(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass#self.columns = columns

    def fit(self, X, y=None):
        return self


    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        new_columns = []
        old_columns = []
        Y = X.copy()
        for x in range(0,Y.shape[1],2):
            two_variables = Y.iloc[:,x:x+2].columns
            old_columns.extend(two_variables)
            mode = two_variables[0].split("_")[0]
            if two_variables[0].split("_")[-1] == 'nhb':
                
                activity = "_".join([two_variables[0].split("_")[-2],two_variables[0].split("_")[-1]])
            else:
                activity = two_variables[0].split("_")[-1]
            
            new_columns.append(f'{mode}_{activity}')
            Y[f'{mode}_{activity}'] = Y.iloc[:,x:x+2].sum(axis=1)
        
        Y = Y.drop(old_columns,axis=1)
        
        old_columns = []
        for x in range(0,Y.shape[1]-8):
            first = Y.iloc[:,x].name
            second = Y.iloc[:,x+8].name
            if first.split("_")[0]==second.split("_")[0]:
                Y[first] = Y[first]+Y[second]
                old_columns.append(second)
                #print(first,second)

        Y = Y.drop(old_columns,axis=1)
               
        X = Y
            
        return X
    
    
class FeatureLogTransform(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
        
    def get_features(self, X):
        return X.columns
    
    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        return np.log1p(X)
    
class TypeSelector(BaseEstimator, TransformerMixin):
    def __init__(self, dtype):
        self.dtype = dtype
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        return X.select_dtypes(include=[self.dtype])


# In[ ]:




