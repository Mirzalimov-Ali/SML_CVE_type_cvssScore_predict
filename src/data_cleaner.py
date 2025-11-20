import re
import unicodedata
from dateutil import parser as dp
import pandas as pd
import numpy as np

RE_CONTROL = re.compile(r'[\x00-\x1f\x7f-\x9f]')
VENDPROD_REGEX = re.compile(
    r'(?:in|affects|affecting|found in|for)\s+([A-Za-z0-9_\-\.]+)[, ]+\s*([A-Za-z0-9_\-\.]+)',
    flags=re.IGNORECASE
)

def clean_description(text):
    if not isinstance(text, str):
        return text
    s = unicodedata.normalize("NFKC", text)
    s = RE_CONTROL.sub(" ", s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_cvss(x):
    try:
        return float(x)
    except Exception:
        m = re.search(r'(\d+(?:\.\d+)?)', str(x))
        return float(m.group(1)) if m else np.nan

def parse_publish_date(x):
    if not x or pd.isna(x):
        return np.nan
    try:
        return dp.parse(str(x)).strftime("%Y-%m-%d")
    except Exception:
        m = re.search(r'(\d{4}-\d{2}-\d{2})', str(x))
        return m.group(1) if m else np.nan

def normalize_cwe(x):
    if not isinstance(x, str):
        return x
    s = x.strip()
    return "NVD-CWE-noinfo" if s.lower() == "nvd-cwe-noinfo" else s

def is_rejected_or_duplicate(desc):
    if not isinstance(desc, str):
        return False
    d = desc.lower()
    if "rejected" in d and "duplicate" in d:
        return True
    if re.search(r'please use cve-\d{4}-\d+', d):
        return True
    return False

def extract_vendor_product_from_desc(desc):
    if not isinstance(desc, str):
        return ("", "")
    m = VENDPROD_REGEX.search(desc)
    return (m.group(1).lower(), m.group(2).lower()) if m else ("", "")

def clean_dataframe(df):
    df = df.copy()

    df["description"] = df["description"].astype(str).apply(clean_description)
    df = df[~df["description"].apply(is_rejected_or_duplicate)].copy()
    
    if "publish_date" in df.columns:
        df["publish_date"] = df["publish_date"].apply(parse_publish_date)
    if "cwe" in df.columns:
        df["cwe"] = df["cwe"].apply(normalize_cwe)

    if "vendor" in df.columns and "product" in df.columns:
        def fill_vp(row):
            v, p = row["vendor"], row["product"]
            if pd.isna(v) or pd.isna(p) or not v or not p:
                ev, ep = extract_vendor_product_from_desc(row["description"])
                if ev: v = ev
                if ep: p = ep
            return v, p

        vp = df.apply(fill_vp, axis=1, result_type="expand")
        df["vendor"], df["product"] = vp[0], vp[1]

    return df
