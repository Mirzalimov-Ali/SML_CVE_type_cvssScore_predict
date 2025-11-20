import streamlit as st
import pandas as pd
import joblib

model = joblib.load("pipeline/final_pipeline.joblib")

st.title("CVE Type and CVSS Score Predictor")

cve_input = {
    'cve_id': st.text_input("CVE ID", "CVE-2023-0000"),
    'description': st.text_area("Description", "SQL injection"),
    'cvss_score': st.text_input("CVSS Score", "Medium"),
    'cwe': st.text_input("CWE", "CWE-79"),
    'vendor': st.text_input("Vendor", "linagora"),
    'product': st.text_input("Product", "twake"),
    'publish_date': st.text_input("Publish Date (YYYY-MM-DD)", "2024-06-01"),
}

user_df = pd.DataFrame([cve_input])

if st.button("Predict"):
    pred = model.predict(user_df)[0]
    st.success(f"Predicted Type: **{pred[0]}**")
    st.success(f"Predicted CVSS Score: **{pred[1]}**")
