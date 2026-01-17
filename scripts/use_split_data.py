import pandas as pd
from sklearn.model_selection import train_test_split
import os

df = pd.read_csv("data/raw/merged/merged_dataset.csv")

# TARGET NaN bo'lgan sample larni O‘CHIRISH
df = df.dropna(subset=['type', 'cvss_score'])

x = df.drop(columns=['type', 'cvss_score'], errors='ignore')
y = df[['type', 'cvss_score']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

os.makedirs("data/split", exist_ok=True)

x_train.to_csv("data/split/x_train.csv", index=False)
x_test.to_csv("data/split/x_test.csv", index=False)
y_train.to_csv("data/split/y_train.csv", index=False)
y_test.to_csv("data/split/y_test.csv", index=False)