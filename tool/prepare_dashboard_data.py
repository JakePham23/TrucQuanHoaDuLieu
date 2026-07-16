"""Trich xuat cot can thiet tu dataset/listings_clean.csv cho dashboard task1/task2.

Chay:  python tool/prepare_dashboard_data.py
Ket qua: dashboard/data/listings_dash.csv (chi giu hang co gia hop le)
"""
import pandas as pd
from pathlib import Path

SRC = Path("dataset/listings_clean.csv")
DST = Path("dashboard/data/listings_dash.csv")

COLS = {
    "id": "id",
    "name": "name",
    "neighbourhood_group_cleansed": "borough",
    "room_type": "room_type",
    "price_numeric": "price",
    "review_scores_rating": "rating",
    "review_scores_value": "value_score",
    "number_of_reviews": "reviews",
    "estimated_occupancy_l365d": "occ",
    "estimated_revenue_l365d": "revenue",
}

df = pd.read_csv(SRC, usecols=list(COLS), low_memory=False)
df = df.rename(columns=COLS)
df = df[df["price"].notna()].copy()

df["name"] = df["name"].fillna("").str.slice(0, 60)
df["price"] = df["price"].round(0).astype(int)
df["revenue"] = df["revenue"].round(0).astype(int)
df["occ"] = df["occ"].astype(int)
df["reviews"] = df["reviews"].astype(int)

DST.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(DST, index=False)
print(f"wrote {DST}: {len(df)} rows, {DST.stat().st_size/1e6:.1f} MB")
