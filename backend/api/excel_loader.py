import pandas as pd
import os
from django.conf import settings

DEFAULT_DATA_PATH = os.path.join(settings.DATA_DIR, "dataset.xlsx")

_df_cache = None


def load_df(path=None):
    """
    Loads dataset.xlsx and caches it for fast repeated access.
    """
    global _df_cache

    if _df_cache is not None:
        return _df_cache

    path = path or DEFAULT_DATA_PATH

    if not os.path.exists(path):
        # Return empty DF if file missing
        return pd.DataFrame(columns=["Year", "Area", "Price", "Demand", "Size"])

    df = pd.read_excel(path, engine="openpyxl")
    df.columns = [col.strip() for col in df.columns]

    # Normalize data
    if "Area" in df.columns:
        df["Area"] = df["Area"].astype(str)

    _df_cache = df
    return df


def filter_by_area(area):
    df = load_df()

    if "Area" not in df.columns:
        return pd.DataFrame()

    return df[df["Area"].str.lower() == area.lower()]


def filter_multiple_areas(areas):
    df = load_df()

    area_list = [a.lower() for a in areas]

    return df[df["Area"].str.lower().isin(area_list)]


def get_trend_for_area(area):
    df = filter_by_area(area)

    if df.empty:
        return []

    # Group by year and compute mean price/demand
    trend = df.groupby("Year")[["Price", "Demand"]].mean().reset_index()

    return trend.to_dict(orient="records")
