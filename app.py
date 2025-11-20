import streamlit as st
import pandas as pd
import joblib

model = joblib.load("pipeline/full_pipeline.joblib")

st.title("CVE Type and CVSS Score Predictor")

cve_input = {
    'cve_id': st.text_input("CVE ID", "CVE-2023-0000"),
    'description': st.text_area("Description", "Due to improper handling of user-controlled data, the application inserts raw input into the page using innerHTML, allowing attackers to execute arbitrary script in the victim’s browser."),
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
