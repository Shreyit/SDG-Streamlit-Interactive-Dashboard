import streamlit as st


def get_sdg_colors(sdg):
    """
    Returns a dictionary of colors for the given SDG.
    bg: Background color for the app (saturated for visibility).
    main: Primary dark color for charts/text.
    light: Lighter accent for charts.
    """
    colors = {
        "SDG 2": {
            "bg": "#FFF9C4",
            "main": "#F57F17",
            "light": "#FFF176",
        },  # Yellow (Background: 200, Main: Dark Orange/Gold)
        "SDG 3": {
            "bg": "#C8E6C9",
            "main": "#2E7D32",
            "light": "#81C784",
        },  # Green (Background: 200, Main: Dark Green)
        "SDG 6": {
            "bg": "#B3E5FC",
            "main": "#0277BD",
            "light": "#4FC3F7",
        },  # Light Blue (Background: 200, Main: Dark Blue)
    }
    return colors.get(sdg, {"bg": "#FFFFFF", "main": "#333333", "light": "#CCCCCC"})


def set_theme(sdg):
    """
    Injects dynamic CSS based on the selected SDG.
    """
    theme = get_sdg_colors(sdg)

    # Inject CSS to change the main container background and widget accents
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-color: {theme['bg']};
    }}
    /* Make the block container transparent to show the background */
    .block-container {{
        background-color: rgba(255,255,255,0.85);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    /* Style headers to match theme */
    h1, h2, h3 {{
        color: {theme['main']} !important;
    }}
    /* --- Widget Theming (Control Panel) --- */
    /* Radio Buttons */
    div[role="radiogroup"] > label > div:first-child {{
        background-color: {theme['light']} !important;
        border-color: {theme['main']} !important;
    }}
    div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {{
        background-color: {theme['main']} !important;
    }}
    
    /* Sliders */
    /* The Thumb/Handle */
    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: {theme['main']} !important;
    }}
    /* The Track (Filled part) */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"] {{
        background-color: {theme['main']} !important; 
    }}
    /* The Labels (Min/Max/Current) - often red by default */
    div[data-testid="stSliderTickBar"] + div div {{
        color: {theme['main']} !important; 
    }}
    
    /* Multiselect Tags */
    .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {theme['light']} !important;
        border-color: {theme['main']} !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] span {{
        color: {theme['main']} !important;
    }}

    /* Selectbox / Multiselect Focus Borders */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stMultiSelect div[data-baseweb="select"] > div {{
        border-color: {theme['main']};
    }}
    
    /* Buttons */
    button[kind="primary"] {{
        background-color: {theme['main']} !important;
        border-color: {theme['main']} !important;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )
