import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from src.logger import get_logger

logger = get_logger('preprocessing', 'preprocessing.log')


class Preprocessing(BaseEstimator, TransformerMixin):
    def __init__(self, df: pd.DataFrame, target=None):
        self.df = df.copy()
        self.target = target if isinstance(target, list) else [target] if target else []
        self.imputers = {}
        self.encoders = {}
        self.scalers = {}

    def fill_missing_values(self, include_targets=False):
        logger.info("Filling missing values...")
        for col in self.df.columns:
            if not include_targets and col in self.target:
                continue

            if self.df[col].dtype == 'object':
                imp = SimpleImputer(strategy='most_frequent')
            else:
                imp = SimpleImputer(strategy='median')
            self.df[col] = imp.fit_transform(self.df[[col]]).squeeze()
            self.imputers[col] = imp
        return self


    def encode(self, include_targets=False):
        logger.info("Encoding categorical features...")
        for col in self.df.columns:
            if not include_targets and col in self.target:
                continue

            if self.df[col].dtype == 'object':
                enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
                self.df[col] = enc.fit_transform(self.df[[col]]).squeeze()
                self.encoders[col] = enc
        return self


    def scale(self):
        logger.info("Scaling numerical features...")
        for col in self.df.columns:
            if col in self.target:
                continue
            if pd.api.types.is_numeric_dtype(self.df[col]):
                scaler = MinMaxScaler()
                self.df[col] = scaler.fit_transform(self.df[[col]])
                self.scalers[col] = scaler
        return self
    
    def transform_new(self, new_df: pd.DataFrame):
        df_copy = new_df.copy()
        for col, imp in self.imputers.items():
            if col in df_copy.columns:
                df_copy[col] = imp.transform(df_copy[[col]]).squeeze()
        for col, enc in self.encoders.items():
            if col in df_copy.columns:
                df_copy[col] = enc.transform(df_copy[[col]]).squeeze()
        for col, scaler in self.scalers.items():
            if col in df_copy.columns:
                df_copy[col] = scaler.transform(df_copy[[col]]).squeeze()
        return df_copy

    def get_dataset(self):
        return self.df


    def __getstate__(self):
        state = self.__dict__.copy()
        if 'logger' in state:
            del state['logger']
        if 'df' in state:
            del state['df']
        return state
    
    def fit(self, X, y=None):
        self.df = X.copy()
        self.fill_missing_values()
        self.encode(include_targets=True)
        self.scale()

        return self

    def transform(self, X):
        return self.transform_new(X)