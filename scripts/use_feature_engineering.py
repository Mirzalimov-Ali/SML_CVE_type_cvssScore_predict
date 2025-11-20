import pandas as pd
import os
from src.feature_engineering import FeatureCreatorTransformer
from joblib import dump
from src.logger import get_logger

logger = get_logger('use_feature_engineering', 'feature_engineering.log')
os.chdir(r'C:\\SML_Projects\\SML_CVE_type_cwe_predict')

df = pd.read_csv('data/filled/filled_dataset.csv')
feature_creator = FeatureCreatorTransformer()
df_features = feature_creator.transform(df)

os.makedirs('data/engineered', exist_ok=True)
df_features.to_csv('data/engineered/engineered_dataset.csv', index=False)
dump(feature_creator, 'pipeline/feature_pipeline.joblib')

logger.info("Feature engineering completed and saved.")
