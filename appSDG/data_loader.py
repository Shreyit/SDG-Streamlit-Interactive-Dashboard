import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data():
    """
    Loads and cleans the real SDG data from SDG_final.csv.
    Applies filtering, mapping, and interpolation.
    """
    # 1. Locate File
    possible_paths = [
        "appSDG/SDG_final.csv",
        "SDG_final.csv",
        os.path.join(os.path.dirname(__file__), "SDG_final.csv"),
    ]

    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break

    if not file_path:
        st.error("Data file 'SDG_final.csv' not found.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

    # 2. Filter for Aggregate Data (avoid double counting)
    # Be more permissive: Keep if value matches target OR is missing/empty (implying total)

    # Sex: Keep BOTHSEX or Null
    if "Sex" in df.columns:
        # Standardize for comparison
        df["Sex"] = df["Sex"].fillna("Total").replace("", "Total")
        # Keep rows that are explicitly BOTHSEX or interpreted as Total (missing)
        # Exclude specific breakdowns like MALE/FEMALE if we can rely on BOTHSEX/Total
        # Exception: Maternal Mortality (3.1.1) is FEMALE only.
        df = df[df["Sex"].isin(["BOTHSEX", "Total", "FEMALE"])]

    # Location: Keep ALLAREA or Null
    if "Location" in df.columns:
        df["Location"] = df["Location"].fillna("Total").replace("", "Total")
        df = df[df["Location"].isin(["ALLAREA", "Total"])]

    # Age: Keep ALLAGE or <5Y (for child metrics) or Null
    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna("Total").replace("", "Total")
        # Indicators like 2.1.2 use ALLAGE.
        # Indicators like 3.2.1/2.2.1 use <5Y.
        # We accept both as valid "aggregates" for their respective indicators.
        df = df[df["Age"].isin(["ALLAGE", "<5Y", "Total"])]

    # 3. Define Mapping from Raw Code to App Display Name
    # Matches utils_constants.py exactly
    CODE_TO_NAME = {
        "2.1.1": "2.1.1 Prevalence of undernourishment (%)",
        "2.2.1": "2.2.1 Prevalence of stunting (height for age <-2 SD) (%)",
        "3.1.1": "3.1.1 Maternal Mortality Ratio (per 100k births)",
        "3.2.1": "3.2.1 Under-5 Mortality Rate (per 1,000 live births)",
        "6.1.1": "6.1.1 Proportion of population using safely managed drinking water services (%)",
        "6.2.1": "6.2.1 Proportion of population using safely managed sanitation services (%)",
    }

    # 4. Filter and Map Indicators
    # Ensure string types and strip whitespace
    if "Indicator" in df.columns:
        df["Indicator"] = df["Indicator"].astype(str).str.strip()
    if "GeoAreaName" in df.columns:
        df["GeoAreaName"] = df["GeoAreaName"].astype(str).str.strip()

    # Ensure 'Indicator' column usually holds the code "2.1.2"
    df = df[df["Indicator"].isin(CODE_TO_NAME.keys())]
    df["Indicator"] = df["Indicator"].map(CODE_TO_NAME)

    # 5. Clean Value Column
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # 6. Filter Target Countries and Assign Region
    SOUTH_ASIA = ["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "Bhutan"]
    SE_ASIA = [
        "Indonesia",
        "Viet Nam",
        "Thailand",
        "Myanmar",
        "Malaysia",
        "Philippines",
        "Singapore",
    ]
    target_countries = SOUTH_ASIA + SE_ASIA
    df = df[df["GeoAreaName"].isin(target_countries)]

    # 7. Deduplicate
    df = (
        df.groupby(["GeoAreaName", "TimePeriod", "Indicator"])["Value"]
        .mean()
        .reset_index()
    )

    # 8. Linear Interpolation
    df_pivot = df.pivot(
        index=["GeoAreaName", "TimePeriod"], columns="Indicator", values="Value"
    ).reset_index()

    full_years = range(2015, 2025)
    countries = df_pivot["GeoAreaName"].unique()
    grid = []
    for country in countries:
        for year in full_years:
            grid.append({"GeoAreaName": country, "TimePeriod": year})
    df_grid = pd.DataFrame(grid)

    df_merged = pd.merge(
        df_grid, df_pivot, on=["GeoAreaName", "TimePeriod"], how="left"
    )

    df_interpolated = (
        df_merged.groupby("GeoAreaName")
        .apply(lambda x: x.interpolate(method="linear", limit_direction="both"))
        .reset_index(drop=True)
    )

    df_final = df_interpolated.melt(
        id_vars=["GeoAreaName", "TimePeriod"], var_name="Indicator", value_name="Value"
    ).dropna(subset=["Value"])

    # 9. Assign Region Column
    country_to_region = {}
    for c in SOUTH_ASIA:
        country_to_region[c] = "South Asia"
    for c in SE_ASIA:
        country_to_region[c] = "South East Asia"

    df_final["Region"] = df_final["GeoAreaName"].map(country_to_region)
    # Fallback to avoid NaNs if any country is missed (though target list prevents this)
    df_final["Region"] = df_final["Region"].fillna("Other")

    return df_final
