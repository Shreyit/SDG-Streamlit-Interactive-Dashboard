import streamlit as st
import pandas as pd
import textwrap
from utils import set_theme
from data_loader import load_data
from components.charts import plot_trend_line, plot_peer_comparison, plot_radar_chart
from components.map import plot_choropleth
from utils_constants import SDG_MAP, INDICATOR_RENAME_MAP, ICON_URLS, get_img_as_base64

# --- 1. CONFIGURATION & THEMES ---
st.set_page_config(page_title="SDG Command Center", layout="wide", page_icon="🌏")

# --- 2. DATA LOADING & PROCESSING ---
df = load_data()

if not df.empty:
    # Rename Indicators to include codes (e.g. 2.1.2 ...)
    df["Indicator"] = df["Indicator"].replace(INDICATOR_RENAME_MAP)

# --- 3. CONTROL CENTER (SIDEBAR & TOP) ---
st.sidebar.title("Control Panel")

# A. SDG Selection (Triggers Color Change)
selected_sdg = st.sidebar.radio("Select Goal:", ["SDG 2", "SDG 3", "SDG 6"], index=1)
set_theme(selected_sdg)  # Apply Color

# B. Indicator Selection (Dependent on SDG)
available_indicators = SDG_MAP[selected_sdg]
selected_indicator = st.sidebar.selectbox("Select Indicator:", available_indicators)

# C. Region & Country Selection
st.sidebar.markdown("---")
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

selected_region = st.sidebar.radio(
    "Select Region:", ["All", "South Asia", "South East Asia"]
)

if selected_region == "South Asia":
    region_options = SOUTH_ASIA.copy()
elif selected_region == "South East Asia":
    region_options = SE_ASIA.copy()
else:
    region_options = list(dict.fromkeys(SOUTH_ASIA + SE_ASIA))

if "India" not in region_options:
    region_options = ["India"] + region_options
else:
    if region_options[0] != "India":
        region_options.remove("India")
        region_options.insert(0, "India")

default_countries = ["India"]
if "Pakistan" in region_options and "Pakistan" not in default_countries:
    default_countries.append("Pakistan")
if (
    selected_region in ["All", "South East Asia"]
    and "Indonesia" in region_options
    and "Indonesia" not in default_countries
):
    default_countries.append("Indonesia")

valid_options = (
    [c for c in region_options if c in df["GeoAreaName"].unique()]
    if not df.empty
    else region_options
)
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    valid_options,
    default=[c for c in default_countries if c in valid_options],
)

# D. Year Range Filter
# D. Year Range Filter
if not df.empty:
    min_year = 2015
    max_year = int(df["TimePeriod"].max())
else:
    min_year, max_year = 2015, 2024

st.sidebar.markdown("---")
year_range = st.sidebar.slider("Time Period:", min_year, max_year, (min_year, max_year))

# Filter Data logic
if not df.empty:
    base_df = df[
        (df["Indicator"] == selected_indicator)
        & (df["TimePeriod"] >= year_range[0])
        & (df["TimePeriod"] <= year_range[1])
    ]
    charts_df = base_df[base_df["GeoAreaName"].isin(selected_countries)]
    map_df = base_df[base_df["GeoAreaName"].isin(valid_options)]
else:
    charts_df = pd.DataFrame()
    map_df = pd.DataFrame()

# --- 4. MAIN DASHBOARD ---
# Title & Icons
c1, c2 = st.columns([0.8, 0.2])
with c1:
    st.title(f"India vs. Asia: {selected_sdg} Analysis")
    # Subtitle moved to specific tabs to avoid cluttering Reference tab
with c2:
    # Display Icon for Selected SDG + Main Logo (High Quality HTML)
    img_selected_b64 = get_img_as_base64(ICON_URLS.get(selected_sdg))
    img_main_b64 = get_img_as_base64(ICON_URLS.get("Main"))

    header_html = f"""
    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px;">
        <img src="data:image/png;base64,{img_selected_b64}" width="90" style="border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <img src="data:image/png;base64,{img_main_b64}" width="120" style="border-radius: 5px;">
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Create Tabs
tab_analytics, tab_map, tab_ref = st.tabs(
    ["Comparative Analytics", "Geospatial View", "Reference & Explanation"]
)

with tab_analytics:
    st.markdown(f"**Focus Indicator:** {selected_indicator}")

    # --- ROW 1: TREND & PEER COMPARISON (Side-by-Side) ---
    col_trend, col_peer = st.columns(2)

    with col_trend:
        plot_trend_line(charts_df, selected_indicator, selected_sdg)

    with col_peer:
        plot_peer_comparison(charts_df, year_range[1], selected_sdg)

    # --- ROW 2: RADAR CHART (Full Width) ---
    st.markdown("---")
    # Pass full DF for context calculations, plus selections
    plot_radar_chart(
        df,
        year_range[1],
        SDG_MAP,
        selected_region,
        selected_countries,
        selected_sdg,
    )

with tab_map:
    st.markdown(f"**Focus Indicator:** {selected_indicator}")
    # Map shows the regional context
    plot_choropleth(map_df, year_range[1])


with tab_ref:
    # Prepare Base64 Images for embedding in HTML
    img_sdg2 = get_img_as_base64(ICON_URLS["SDG 2"])
    img_sdg3 = get_img_as_base64(ICON_URLS["SDG 3"])
    img_sdg6 = get_img_as_base64(ICON_URLS["SDG 6"])

    # We strip newlines to prevent Streamlit/Markdown from interpreting indented nested HTML as code blocks
    html_content = f"""
    <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #333;">
        <h3 style="margin-top: 0; color: #333;">Methodology, Explanations & References</h3>
        <div style="margin-top: 1.5rem;">
            <h4 style="color: #444;">Indicator Definitions</h4>
            <ul style="line-height: 1.6; padding-left: 20px;">
                <li><strong>2.1.1 Undernourishment:</strong> Prevalence of undernourishment (%). <em>Target: Zero Hunger.</em></li>
                <li><strong>2.2.1 Stunting (Child):</strong> Prevalence of stunting (height for age <-2 SD). <em>Target: Zero Hunger.</em></li>
                <li><strong>3.1.1 Maternal Mortality:</strong> Ratio per 100k births. <em>Target: Good Health.</em></li>
                <li><strong>3.2.1 Under-5 Mortality:</strong> Rate per 1,000 live births. <em>Target: Good Health.</em></li>
                <li><strong>6.1.1 Drinking Water:</strong> Population using safely managed drinking water services. <em>Target: Clean Water.</em></li>
                <li><strong>6.2.1 Sanitation:</strong> Population using safely managed sanitation services. <em>Target: Clean Water.</em></li>
            </ul>
        </div>
        <div style="margin-top: 1.5rem;">
            <h4 style="color: #444;">Data Sources</h4>
            <ul style="line-height: 1.6; padding-left: 20px;">
                <li><strong>Primary Source:</strong> UN SDG Global Database & World Bank Indices.</li>
                <li><strong>Calculation Method:</strong> Regional averages are calculated as unweighted means of available country data in South and Southeast Asia.</li>
                <li><strong>Interpolation:</strong> Linear interpolation used for missing intermediate years to provide smooth trend lines.</li>
                <li><strong>Map Source:</strong> DataMeet (India Boundaries) & Carto/OpenStreetMap (Base Tiles).</li>
            </ul>
        </div>
        <div style="margin-top: 2rem;">
            <h4 style="color: #444;">SDG Goals at a Glance</h4>
            <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 1rem;">
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{img_sdg2}" width="100" style="margin-bottom: 5px;">
                    <br><small><strong>Goal 2: Zero Hunger</strong></small>
                </div>
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{img_sdg3}" width="100" style="margin-bottom: 5px;">
                    <br><small><strong>Goal 3: Good Health</strong></small>
                </div>
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{img_sdg6}" width="100" style="margin-bottom: 5px;">
                    <br><small><strong>Goal 6: Clean Water</strong></small>
                </div>
            </div>
        </div>
    </div>
    """.replace(
        "\n", ""
    )

    st.markdown(html_content, unsafe_allow_html=True)
