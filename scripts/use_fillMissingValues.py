import pandas as pd
import os
from joblib import dump
from src.preprocessing import Preprocessing
from src.logger import get_logger

logger = get_logger('use_fillMissingValues', 'preprocessing.log')
os.chdir(r'C:\\SML_Projects\\SML_CVE_type_cwe_predict')

df = pd.read_csv('data/raw/merged/merged_dataset.csv')
logger.info(f"Loaded dataset with shape {df.shape}")

preprocessing = Preprocessing(df, target=['type', 'cvss_score'])
df_filled = preprocessing.fill_missing_values(include_targets=True).get_dataset()

os.makedirs('data/filled', exist_ok=True)
dump(preprocessing, 'pipeline/filled_pipeline.joblib')
df_filled.to_csv('data/filled/filled_dataset.csv', index=False)

logger.info("Saved filled dataset and pipeline.")