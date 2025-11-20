import os
import pandas as pd
from src.data_extraction import DataExtractor
from src.data_cleaner import clean_dataframe
from src.logger import get_logger

logger = get_logger('use_data_extraction', 'data_extraction.log')

YEARS = [2023, 2024, 2025]
FEED_URL = "https://nvd.nist.gov/feeds/json/cve/2.0/"
API_KEY = os.getenv("NVD_API_KEY", "").strip()

extractor = DataExtractor(years=YEARS)
total_raw, total_clean = 0, 0

extracted_folder = os.path.join("data/raw/extracted")
cleaned_folder = os.path.join("data/raw/cleaned")

os.makedirs(extracted_folder, exist_ok=True)
os.makedirs(cleaned_folder, exist_ok=True)

for y in YEARS:
    try:
        raw_data = extractor.fetch_feed_year(y, FEED_URL, API_KEY)
        raw_df = pd.DataFrame(raw_data)
        total_raw += len(raw_df)

        # Save extracted dataset
        raw_out = os.path.join(extracted_folder, f"cve_{y}_dataset.csv")
        raw_df.to_csv(raw_out, index=False, encoding="utf-8", quoting=1, escapechar='\\')

        print(f"{y}: {len(raw_df)} rows fetched and saved to {raw_out}")
        logger.info(f"{y}: {len(raw_df)} rows fetched and saved to {raw_out}")

        clean_df = clean_dataframe(raw_df)
        clean_df["type"] = clean_df.apply(lambda r: extractor.classify(r["cwe"], r["description"]), axis=1)
        total_clean += len(clean_df)

        # Save cleaned dataset
        clean_out = os.path.join(cleaned_folder, f"cleaned_cve_{y}_dataset.csv")
        clean_df.to_csv(clean_out, index=False, encoding="utf-8", quoting=1, escapechar='\\')
        
        print(f"{y}: {len(clean_df)} rows cleaned and saved to {clean_out}")
        logger.info(f"{y}: {len(clean_df)} rows cleaned and saved to {clean_out}")

    except Exception as e:
        logger.error(f"{y}: {e}")
        print(f"{y}: {e}")

print(f"\nTotal fetched: {total_raw} rows")
print(f"Total cleaned: {total_clean} rows")
logger.info(f"Total fetched: {total_raw}, Total cleaned: {total_clean}")