import pandas as pd
import os
from joblib import load, dump
from src.preprocessing import Preprocessing
from src.logger import get_logger

logger = get_logger('use_preprocessing', 'preprocessing.log')
os.chdir(r'C:\\SML_Projects\\SML_CVE_type_cwe_predict')

df = pd.read_csv('data/engineered/engineered_dataset.csv')
preprocessing = Preprocessing(df, target=['type', 'cvss_score'])

df_preprocessed = (
    preprocessing.encode()
    .scale()
    .get_dataset()
)

os.makedirs('data/preprocessed', exist_ok=True)
df_preprocessed.to_csv('data/preprocessed/preprocessed_dataset.csv', index=False)
dump(preprocessing, 'pipeline/preprocessed_pipeline.joblib')

logger.info("Encoding and scaling completed and saved.")