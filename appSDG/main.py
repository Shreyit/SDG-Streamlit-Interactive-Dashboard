import streamlit as st
import pandas as pd
import textwrap
from utils import set_theme, get_sdg_colors
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
    theme = get_sdg_colors(selected_sdg)
    img_sdg2 = get_img_as_base64(ICON_URLS["SDG 2"])
    img_sdg3 = get_img_as_base64(ICON_URLS["SDG 3"])
    img_sdg6 = get_img_as_base64(ICON_URLS["SDG 6"])

    m = theme["main"]
    lt = theme["light"]
    bdr = theme["border"]
    gl = theme["glass"]
    acc = theme["accent"]
    rgb = theme["rgb"]

    ref_html = f"""
<style>
.ref-page {{ font-family: 'Inter', sans-serif; color: #222; }}
.ref-hero {{
  background: linear-gradient(135deg, rgba({rgb},0.12) 0%, rgba({rgb},0.04) 100%);
  border: 1px solid {bdr};
  border-radius: 20px;
  padding: 1.8rem 2rem;
  margin-bottom: 1.6rem;
  position: relative;
  overflow: hidden;
}}
.ref-hero::before {{
  content: '';
  position: absolute;
  width: 300px; height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba({rgb},0.18), transparent 70%);
  top: -100px; right: -80px;
  pointer-events: none;
}}
.ref-hero-badge {{
  display: inline-block;
  background: {m};
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 0.7rem;
}}
.ref-hero h2 {{
  margin: 0 0 0.4rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: {m};
}}
.ref-hero p {{
  margin: 0;
  color: #555;
  font-size: 0.9rem;
  max-width: 620px;
}}
.sec-label {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.05rem;
  font-weight: 700;
  color: {m};
  margin: 1.6rem 0 0.9rem;
  border-left: 4px solid {m};
  padding-left: 10px;
}}
.countries-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 0.4rem;
}}
.region-card {{
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid {bdr};
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 18px rgba({rgb},0.08);
}}
.region-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.7rem 1rem;
  font-weight: 700;
  font-size: 0.88rem;
  color: #fff;
}}
.rh-sa {{ background: linear-gradient(90deg, #1B5E20, #43A047); }}
.rh-sea {{ background: linear-gradient(90deg, #0D47A1, #1E88E5); }}
.count-pill {{
  background: rgba(255,255,255,0.28);
  border: 1px solid rgba(255,255,255,0.45);
  border-radius: 20px;
  padding: 2px 9px;
  font-size: 0.7rem;
  font-weight: 600;
}}
.country-list {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 0.8rem 1rem;
}}
.country-chip {{
  background: {acc};
  border: 1px solid {bdr};
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 0.78rem;
  font-weight: 500;
  color: #333;
  white-space: nowrap;
}}
.country-chip.focus {{
  background: {m};
  border-color: {m};
  color: #fff;
  font-weight: 700;
}}
.indicators-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 0.4rem;
}}
.ind-card {{
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.07);
}}
.ind-card-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.7rem 0.9rem;
  font-weight: 700;
  font-size: 0.82rem;
  color: #fff;
}}
.ih-sdg2 {{ background: linear-gradient(90deg, #E65100, #FF8F00); }}
.ih-sdg3 {{ background: linear-gradient(90deg, #1B5E20, #43A047); }}
.ih-sdg6 {{ background: linear-gradient(90deg, #0D47A1, #1E88E5); }}
.ind-card ul {{
  margin: 0;
  padding: 0.7rem 0.9rem 0.7rem 1.6rem;
  list-style: disc;
}}
.ind-card ul li {{
  font-size: 0.78rem;
  color: #444;
  line-height: 1.55;
  margin-bottom: 3px;
}}
.ind-card ul li strong {{ color: #222; }}
.meth-steps {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.8rem;
  margin-bottom: 0.4rem;
}}
.meth-step {{
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(10px);
  border: 1px solid {bdr};
  border-radius: 14px;
  padding: 0.85rem 1rem;
  box-shadow: 0 2px 10px rgba({rgb},0.06);
}}
.step-num {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px; height: 26px;
  border-radius: 50%;
  background: {m};
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}}
.step-title {{
  font-weight: 700;
  font-size: 0.82rem;
  color: {m};
  margin-bottom: 3px;
}}
.step-desc {{
  font-size: 0.76rem;
  color: #666;
  line-height: 1.45;
}}
.refs-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.8rem;
  margin-bottom: 0.4rem;
}}
.ref-card {{
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(10px);
  border: 1px solid {bdr};
  border-radius: 14px;
  padding: 0.85rem 1rem;
  box-shadow: 0 2px 10px rgba({rgb},0.06);
  transition: box-shadow 0.2s, transform 0.2s;
}}
.ref-card:hover {{
  box-shadow: 0 6px 22px rgba({rgb},0.14);
  transform: translateY(-2px);
}}
.ref-card-logo {{
  font-size: 1.4rem;
  margin-bottom: 0.35rem;
}}
.ref-card-name {{
  font-weight: 700;
  font-size: 0.82rem;
  color: {m};
  margin-bottom: 3px;
}}
.ref-card-desc {{
  font-size: 0.74rem;
  color: #666;
  line-height: 1.45;
}}
.goals-row {{
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 0.4rem;
  flex-wrap: wrap;
}}
.goal-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.70);
  border: 1px solid {bdr};
  border-radius: 16px;
  padding: 1rem 1.4rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 14px rgba({rgb},0.07);
  transition: transform 0.2s;
}}
.goal-item:hover {{ transform: translateY(-3px); }}
.goal-label {{
  font-size: 0.78rem;
  font-weight: 600;
  color: #444;
  text-align: center;
}}
</style>
<div class="ref-page">

  <div class="ref-hero">
    <div class="ref-hero-badge">UN Sustainable Development Goals</div>
    <h2>Methodology, Explanations &amp; References</h2>
    <p>Tracking South Asia &amp; South East Asia's progress across SDG Goals 2, 3, and 6 — covering food security, child nutrition, health outcomes, and access to water &amp; sanitation (2015–2024).</p>
  </div>

  <!-- COUNTRIES -->
  <div class="sec-label">🌏 Country Coverage</div>
  <div class="countries-grid">
    <div class="region-card">
      <div class="region-header rh-sa">South Asia <span class="count-pill">6 Countries</span></div>
      <div class="country-list">
        <span class="country-chip focus">🇮🇳 India</span>
        <span class="country-chip">🇵🇰 Pakistan</span>
        <span class="country-chip">🇧🇩 Bangladesh</span>
        <span class="country-chip">🇳🇵 Nepal</span>
        <span class="country-chip">🇱🇰 Sri Lanka</span>
        <span class="country-chip">🇧🇹 Bhutan</span>
      </div>
    </div>
    <div class="region-card">
      <div class="region-header rh-sea">South East Asia <span class="count-pill">7 Countries</span></div>
      <div class="country-list">
        <span class="country-chip">🇮🇩 Indonesia</span>
        <span class="country-chip">🇻🇳 Viet Nam</span>
        <span class="country-chip">🇹🇭 Thailand</span>
        <span class="country-chip">🇲🇲 Myanmar</span>
        <span class="country-chip">🇲🇾 Malaysia</span>
        <span class="country-chip">🇵🇭 Philippines</span>
        <span class="country-chip">🇸🇬 Singapore</span>
      </div>
    </div>
  </div>

  <!-- INDICATORS -->
  <div class="sec-label">📊 SDG Indicators Tracked</div>
  <div class="indicators-grid">
    <div class="ind-card">
      <div class="ind-card-header ih-sdg2">
        <img src="data:image/png;base64,{img_sdg2}" width="32" style="border-radius:4px;">
        Goal 2: Zero Hunger
      </div>
      <ul>
        <li><strong>2.1.1</strong> Prevalence of undernourishment (%)</li>
        <li><strong>2.2.1</strong> Prevalence of stunting in children under 5 (height-for-age &lt; -2 SD) (%)</li>
      </ul>
    </div>
    <div class="ind-card">
      <div class="ind-card-header ih-sdg3">
        <img src="data:image/png;base64,{img_sdg3}" width="32" style="border-radius:4px;">
        Goal 3: Good Health
      </div>
      <ul>
        <li><strong>3.1.1</strong> Maternal Mortality Ratio (per 100,000 live births)</li>
        <li><strong>3.2.1</strong> Under-5 Mortality Rate (per 1,000 live births)</li>
      </ul>
    </div>
    <div class="ind-card">
      <div class="ind-card-header ih-sdg6">
        <img src="data:image/png;base64,{img_sdg6}" width="32" style="border-radius:4px;">
        Goal 6: Clean Water
      </div>
      <ul>
        <li><strong>6.1.1</strong> Population using safely managed drinking water services (%)</li>
        <li><strong>6.2.1</strong> Population using safely managed sanitation services (%)</li>
      </ul>
    </div>
  </div>

  <!-- METHODOLOGY -->
  <div class="sec-label">⚙️ Methodology</div>
  <div class="meth-steps">
    <div class="meth-step">
      <div class="step-num">1</div>
      <div class="step-title">Source</div>
      <div class="step-desc">Raw data ingested from the UN SDG Global Indicator Database (SDG_final.csv) covering 2000–2024.</div>
    </div>
    <div class="meth-step">
      <div class="step-num">2</div>
      <div class="step-title">Aggregate Filter</div>
      <div class="step-desc">Rows filtered to aggregate disaggregations only: BOTHSEX, ALLAREA, ALLAGE (or &lt;5Y for child metrics) to prevent double-counting.</div>
    </div>
    <div class="meth-step">
      <div class="step-num">3</div>
      <div class="step-title">Deduplication</div>
      <div class="step-desc">Where multiple values remain per country-year-indicator, the mean is taken to produce a single representative value.</div>
    </div>
    <div class="meth-step">
      <div class="step-num">4</div>
      <div class="step-title">Interpolation</div>
      <div class="step-desc">Linear interpolation (both directions) fills gaps in the 2015–2024 window, producing smooth trend lines per country.</div>
    </div>
  </div>

  <!-- REFERENCES -->
  <div class="sec-label">🔗 Data Sources &amp; References</div>
  <div class="refs-grid">
    <div class="ref-card">
      <div class="ref-card-logo">🇺🇳</div>
      <div class="ref-card-name">UN SDG Global Database</div>
      <div class="ref-card-desc">Primary data source. Official custodian datasets for all 6 indicators. unstats.un.org/sdgs/dataportal</div>
    </div>
    <div class="ref-card">
      <div class="ref-card-logo">🏦</div>
      <div class="ref-card-name">World Bank Open Data</div>
      <div class="ref-card-desc">Cross-validation reference and supplementary socioeconomic context. data.worldbank.org</div>
    </div>
    <div class="ref-card">
      <div class="ref-card-logo">🏥</div>
      <div class="ref-card-name">WHO Global Health Observatory</div>
      <div class="ref-card-desc">Maternal and child health indicator validation. who.int/data/gho</div>
    </div>
    <div class="ref-card">
      <div class="ref-card-logo">🧒</div>
      <div class="ref-card-name">UNICEF Data</div>
      <div class="ref-card-desc">Stunting and under-5 mortality cross-reference. data.unicef.org</div>
    </div>
    <div class="ref-card">
      <div class="ref-card-logo">🇮🇳</div>
      <div class="ref-card-name">NITI Aayog SDG India Index</div>
      <div class="ref-card-desc">India-specific SDG progress benchmarks and state-level data. sdgindiaindex.niti.gov.in</div>
    </div>
    <div class="ref-card">
      <div class="ref-card-logo">🗺️</div>
      <div class="ref-card-name">Natural Earth / OpenStreetMap</div>
      <div class="ref-card-desc">Base map tiles via Carto Positron. Country boundaries via Johan world.geo.json (international standard). naturalearth.com</div>
    </div>
  </div>

  <!-- SDG GOALS AT A GLANCE -->
  <div class="sec-label">🎯 SDG Goals at a Glance</div>
  <div class="goals-row">
    <div class="goal-item">
      <img src="data:image/png;base64,{img_sdg2}" width="90" style="border-radius:8px;">
      <span class="goal-label">Goal 2<br>Zero Hunger</span>
    </div>
    <div class="goal-item">
      <img src="data:image/png;base64,{img_sdg3}" width="90" style="border-radius:8px;">
      <span class="goal-label">Goal 3<br>Good Health &amp; Well-Being</span>
    </div>
    <div class="goal-item">
      <img src="data:image/png;base64,{img_sdg6}" width="90" style="border-radius:8px;">
      <span class="goal-label">Goal 6<br>Clean Water &amp; Sanitation</span>
    </div>
  </div>

</div>
"""

    st.markdown(ref_html, unsafe_allow_html=True)
