import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

MODEL_PATH = Path("pipeline/full_pipeline.joblib")

app = FastAPI(
    title="CVE Attack Type & CVSS Prediction API",
    version="1.0"
)

pipeline = None


# --------------------------------------------------
# Load model ON STARTUP
# --------------------------------------------------
@app.on_event("startup")
def load_model():
    global pipeline
    try:
        pipeline = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load model: {e}")


# --------------------------------------------------
# Schemas
# --------------------------------------------------
class CVEInput(BaseModel):
    cve_id: str
    description: str
    cwe: str
    vendor: str
    product: str
    publish_date: str


class PredictionOutput(BaseModel):
    attack_type: str
    cvss_score: str


# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------------------------------------
# Predict
# --------------------------------------------------
@app.post("/predict", response_model=PredictionOutput)
def predict(data: CVEInput):

    if pipeline is None:
        raise RuntimeError("Model not loaded")

    df = pd.DataFrame([data.model_dump()])

    pred = pipeline.predict(df)[0]

    return {
        "attack_type": str(pred[0]),
        "cvss_score": str(pred[1])
    }