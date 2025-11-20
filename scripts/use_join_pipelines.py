from joblib import load, dump
from sklearn.pipeline import Pipeline

fill_pipe = load('pipeline/filled_pipeline.joblib')
feat_pipe = load('pipeline/feature_pipeline.joblib')
prep_pipe = load('pipeline/preprocessed_pipeline.joblib')
model = load('pipeline/final_pipeline.joblib')

full_pipeline = Pipeline([
    ('fill', fill_pipe),
    ('feature', feat_pipe),
    ('prep', prep_pipe),
    ('model', model)
])

dump(full_pipeline, 'pipeline/full_pipeline.joblib')
print("Full pipeline saved as 'full_pipeline.joblib'")