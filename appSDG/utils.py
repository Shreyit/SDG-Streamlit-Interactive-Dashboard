import streamlit as st


def get_sdg_colors(sdg):
    colors = {
        "SDG 2": {
            "bg": "#FFFDF0",
            "bg_end": "#FFF3CD",
            "main": "#E65100",
            "light": "#FF8F00",
            "accent": "#FFF8E1",
            "glass": "rgba(230, 81, 0, 0.08)",
            "border": "rgba(230, 81, 0, 0.2)",
            "rgb": "230, 81, 0",
            "orb": "rgba(255, 160, 0, 0.28)",
        },
        "SDG 3": {
            "bg": "#F1FBF2",
            "bg_end": "#DCEDC8",
            "main": "#1B5E20",
            "light": "#2E7D32",
            "accent": "#E8F5E9",
            "glass": "rgba(27, 94, 32, 0.08)",
            "border": "rgba(27, 94, 32, 0.2)",
            "rgb": "27, 94, 32",
            "orb": "rgba(76, 175, 80, 0.28)",
        },
        "SDG 6": {
            "bg": "#F0F7FF",
            "bg_end": "#BBDEFB",
            "main": "#0D47A1",
            "light": "#1565C0",
            "accent": "#E3F2FD",
            "glass": "rgba(13, 71, 161, 0.08)",
            "border": "rgba(13, 71, 161, 0.2)",
            "rgb": "13, 71, 161",
            "orb": "rgba(33, 150, 243, 0.28)",
        },
    }
    return colors.get(
        sdg,
        {
            "bg": "#F5F5F5",
            "bg_end": "#E0E0E0",
            "main": "#333333",
            "light": "#555555",
            "accent": "#EEEEEE",
            "glass": "rgba(0,0,0,0.05)",
            "border": "rgba(0,0,0,0.12)",
            "rgb": "51,51,51",
            "orb": "rgba(100,100,100,0.2)",
        },
    )


def set_theme(sdg):
    theme = get_sdg_colors(sdg)

    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    *, *::before, *::after {{ font-family: 'Inter', sans-serif !important; }}

    /* ── BACKGROUND ── */
    .stApp {{
        background: linear-gradient(160deg, {theme['bg']} 0%, {theme['bg_end']} 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        width: 650px; height: 650px;
        border-radius: 50%;
        background: radial-gradient(circle, {theme['orb']} 0%, transparent 68%);
        top: -200px; right: -200px;
        pointer-events: none;
        z-index: 0;
    }}
    .stApp::after {{
        content: '';
        position: fixed;
        width: 450px; height: 450px;
        border-radius: 50%;
        background: radial-gradient(circle, {theme['orb']} 0%, transparent 68%);
        bottom: -120px; left: -120px;
        pointer-events: none;
        z-index: 0;
    }}

    /* ── MAIN GLASS CONTAINER ── */
    .block-container {{
        background: rgba(255, 255, 255, 0.76);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border: 1px solid {theme['border']};
        border-radius: 24px;
        padding: 2rem 2.5rem 3rem;
        margin-top: 1rem;
        box-shadow:
            0 8px 40px rgba({theme['rgb']}, 0.10),
            0 2px 8px rgba(0,0,0,0.06),
            inset 0 1px 0 rgba(255,255,255,0.9);
        position: relative;
        z-index: 1;
    }}

    /* ── TYPOGRAPHY ── */
    h1 {{
        color: {theme['main']} !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px !important;
        line-height: 1.2 !important;
    }}
    h2 {{
        color: {theme['main']} !important;
        font-weight: 700 !important;
    }}
    h3 {{
        color: {theme['light']} !important;
        font-weight: 600 !important;
    }}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.68) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid {theme['border']} !important;
        box-shadow: 4px 0 24px rgba({theme['rgb']}, 0.08);
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
        color: {theme['main']} !important;
    }}

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.55) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
        border: 1px solid {theme['border']};
        box-shadow: 0 2px 14px rgba({theme['rgb']}, 0.07);
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: #666 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.22s ease !important;
        padding: 8px 22px !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: {theme['glass']} !important;
        color: {theme['main']} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba({theme['rgb']}, 0.13) !important;
        color: {theme['main']} !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 10px rgba({theme['rgb']}, 0.18) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ── RADIO BUTTONS ── */
    div[role="radiogroup"] > label > div:first-child {{
        background-color: {theme['glass']} !important;
        border-color: {theme['border']} !important;
    }}
    div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {{
        background-color: {theme['main']} !important;
    }}

    /* ── SLIDER ── */
    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: {theme['main']} !important;
        box-shadow: 0 0 0 4px rgba({theme['rgb']}, 0.2) !important;
    }}

    /* ── MULTISELECT TAGS ── */
    .stMultiSelect span[data-baseweb="tag"] {{
        background: rgba({theme['rgb']}, 0.10) !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 8px !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] span {{
        color: {theme['main']} !important;
        font-weight: 500 !important;
    }}

    /* ── SELECT / MULTISELECT INPUT ── */
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        border-color: {theme['border']} !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.82) !important;
    }}

    /* ── METRIC CARDS ── */
    [data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 14px !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 2px 12px rgba({theme['rgb']}, 0.08) !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {theme['main']} !important;
        font-weight: 700 !important;
    }}

    /* ── DIVIDER ── */
    hr {{
        border-color: {theme['border']} !important;
        opacity: 0.55;
    }}

    /* ── PRIMARY BUTTON ── */
    button[kind="primary"] {{
        background: linear-gradient(135deg, {theme['main']}, {theme['light']}) !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba({theme['rgb']}, 0.30) !important;
        font-weight: 600 !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease !important;
    }}
    button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba({theme['rgb']}, 0.40) !important;
    }}

    /* ── PLOTLY CHART WRAPPER ── */
    [data-testid="stPlotlyChart"] > div {{
        background: rgba(255, 255, 255, 0.62) !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 18px !important;
        padding: 4px !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 18px rgba({theme['rgb']}, 0.08) !important;
        overflow: hidden;
    }}

    /* ── SUBHEADER LEFT ACCENT ── */
    [data-testid="stSubheader"] {{
        color: {theme['main']} !important;
        font-weight: 700 !important;
        border-left: 4px solid {theme['main']};
        padding-left: 10px !important;
        margin-bottom: 0.6rem !important;
    }}

    /* ── ALERT / INFO BOXES ── */
    [data-testid="stAlert"] {{
        border-radius: 12px !important;
        border-left: 4px solid {theme['main']} !important;
        background: {theme['accent']} !important;
    }}

    /* ── FOCUS RING ── */
    *:focus-visible {{
        outline: 2px solid {theme['main']} !important;
        outline-offset: 2px;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )
