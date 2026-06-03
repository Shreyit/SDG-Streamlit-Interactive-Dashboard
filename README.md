# SDG Command Center: South & Southeast Asia Analysis

A high-fidelity interactive dashboard for analyzing Sustainable Development Goals (SDG 2, 3, 6) across South and Southeast Asia, with a specific focus on India. Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge.svg)](https://sdg-app-interactive-dashboard-sygs673mdaxne7qflxpvgc.streamlit.app/?embed_options=light_theme)

**Live Dashboard:** [View the Interactive SDG Command Center](https://sdg-app-interactive-dashboard-sygs673mdaxne7qflxpvgc.streamlit.app/?embed_options=light_theme)
**GitHub Repository:** [Shreyit/SDG-Streamlit-Interactive-Dashboard](https://github.com/Shreyit/SDG-Streamlit-Interactive-Dashboard)

---

## Features

- **Glassmorphism UI**: Frosted-glass containers, SDG-tinted gradient backgrounds, and decorative radial orbs — inspired by the NITI Aayog SDG India Index and UN SDG website.
- **Dynamic Theming**: Colors and accents shift automatically with the selected SDG (Amber → SDG 2, Green → SDG 3, Blue → SDG 6).
- **Comparative Analytics**: Trend lines, peer comparison bar charts, and a multi-goal Radar Chart (SDG 2, 3, 6 combined).
- **Geospatial View**: Regional choropleth map across 13 countries in South & Southeast Asia.
- **Reference & Methodology Tab**: Countries by region, per-SDG indicator cards, 4-step methodology breakdown, and 6 cited data sources.
- **Data Integrity**: Linear interpolation fills year gaps; aggregate-only disaggregations (BOTHSEX, ALLAREA, ALLAGE) prevent double-counting.

---

## Country Coverage

| Region | Countries |
| --- | --- |
| **South Asia** | 🇮🇳 India · 🇵🇰 Pakistan · 🇧🇩 Bangladesh · 🇳🇵 Nepal · 🇱🇰 Sri Lanka · 🇧🇹 Bhutan |
| **South East Asia** | 🇮🇩 Indonesia · 🇻🇳 Viet Nam · 🇹🇭 Thailand · 🇲🇲 Myanmar · 🇲🇾 Malaysia · 🇵🇭 Philippines · 🇸🇬 Singapore |

---

## SDG Indicators Tracked

| Goal | Code | Indicator |
| --- | --- | --- |
| **SDG 2 – Zero Hunger** | 2.1.1 | Prevalence of undernourishment (%) |
| | 2.2.1 | Prevalence of stunting in children under 5 (%) |
| **SDG 3 – Good Health** | 3.1.1 | Maternal Mortality Ratio (per 100,000 live births) |
| | 3.2.1 | Under-5 Mortality Rate (per 1,000 live births) |
| **SDG 6 – Clean Water** | 6.1.1 | Population using safely managed drinking water (%) |
| | 6.2.1 | Population using safely managed sanitation (%) |

---

## Map — India Boundary Notice

The geospatial view uses the standard **Natural Earth / OpenStreetMap** boundary dataset. The complete, legally accurate boundary of India (including Jammu & Kashmir, Aksai Chin, and other territories) is **intentionally not rendered** via any open-source GeoJSON, as depicting an incorrect or incomplete map of India in a public-facing application is a punishable offence under **Government of India guidelines**. A certified boundary file is therefore excluded from this open-source project.

---

## Installation & Running Locally

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Shreyit/SDG-Streamlit-Interactive-Dashboard.git
   cd SDG-Streamlit-Interactive-Dashboard
   ```

2. **Install dependencies**:

   ```bash
   pip install -r appSDG/requirements.txt
   ```

3. **Run the app**:

   ```bash
   streamlit run appSDG/main.py
   ```

---

## Project Structure

```text
appSDG/
├── main.py               # App entry point — layout, sidebar, tab routing
├── data_loader.py        # CSV ingestion, filtering, deduplication, interpolation
├── utils.py              # Glassmorphism CSS theme engine
├── utils_constants.py    # SDG mappings, icon paths, helper functions
├── SDG_final.csv         # Processed UN SDG source data
├── requirements.txt      # Python dependencies
├── components/
│   ├── charts.py         # Trend, peer comparison, and radar chart definitions
│   └── map.py            # Choropleth map + India boundary notice
└── assets/               # Official SDG icons (UN Communications Guidelines)
```

---

## Data Sources & References

| Source | Use |
| --- | --- |
| [UN SDG Global Database](https://unstats.un.org/sdgs/dataportal) | Primary data for all 6 indicators |
| [World Bank Open Data](https://data.worldbank.org) | Cross-validation reference |
| [WHO Global Health Observatory](https://www.who.int/data/gho) | Maternal & child health validation |
| [UNICEF Data](https://data.unicef.org) | Stunting & under-5 mortality cross-reference |
| [NITI Aayog SDG India Index](https://sdgindiaindex.niti.gov.in) | India-specific SDG benchmarks |
| [Natural Earth](https://www.naturalearthdata.com) | Base map tiles (Carto Positron) |

---

## Changelog

### v2.0

- Glassmorphism UI redesign — gradient backgrounds, frosted glass containers, decorative orbs
- Reference tab rebuilt: country coverage grid, SDG indicator cards, methodology steps, 6 cited sources
- Geospatial map: removed legally non-compliant India composite GeoJSON overlay; added India boundary disclaimer; fixed `Viet Nam` → `Vietnam` name mapping for world GeoJSON
- Fixed `KeyError` crash on Streamlit Cloud (Python 3.13 / pandas 3.x): replaced `groupby().apply()` with `groupby().transform()` in data interpolation

### v1.0

- Initial release with SDG 2, 3, 6 indicators across South & Southeast Asia
- Trend lines, peer comparison, radar chart, choropleth map

---

## Credits

- **Icons**: Official SDG Icons — UN Communications Guidelines
- **Inspiration**: [NITI Aayog SDG India Index](https://sdgindiaindex.niti.gov.in) · [UN SDG Website](https://sdgs.un.org)
