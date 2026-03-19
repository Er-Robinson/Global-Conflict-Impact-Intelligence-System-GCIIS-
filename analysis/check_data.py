import pandas as pd

df = pd.read_csv("data/raw/news/news_2026-03-18.csv")

print(df.columns)
print(df.head())