import plotly.express as px
import streamlit as st

WORLD_GEOJSON_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
)

# The Johan world GeoJSON uses slightly different country names than the UN SDG database.
# This mapping normalises the dataset names before plotting.
GEO_NAME_FIX = {
    "Viet Nam": "Vietnam",
}


def plot_choropleth(df, year):
    st.subheader(f"Geospatial View: ({year})")

    if df.empty:
        st.warning("No data available for map.")
        return

    map_data = df[df["TimePeriod"] == year].copy()

    if map_data.empty:
        st.warning(f"No data available for map in year {year}.")
        return

    # Normalise country names to match the GeoJSON
    map_data["GeoAreaName"] = map_data["GeoAreaName"].replace(GEO_NAME_FIX)

    fig = px.choropleth_mapbox(
        map_data,
        geojson=WORLD_GEOJSON_URL,
        locations="GeoAreaName",
        featureidkey="properties.name",
        color="Value",
        color_continuous_scale="Plasma",
        range_color=(map_data["Value"].min(), map_data["Value"].max()),
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 15, "lon": 100},
        opacity=0.82,
        labels={"Value": "Value"},
        hover_name="GeoAreaName",
        hover_data={"Value": ":.2f", "GeoAreaName": False},
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Value",
            thickness=14,
            len=0.6,
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div style="
            background: rgba(255,193,7,0.10);
            border: 1px solid rgba(255,193,7,0.45);
            border-left: 4px solid #f9a825;
            border-radius: 10px;
            padding: 0.65rem 1rem;
            margin-top: 0.4rem;
            font-size: 0.82rem;
            color: #555;
            line-height: 1.5;
        ">
        ⚠️ <strong>Map Note (India):</strong>
        India is rendered here using standard boundaries as provided by the
        <em>Johan world GeoJSON</em> (sourced from Natural Earth / OpenStreetMap).
        This open-source dataset does <strong>not</strong> depict the complete,
        legally accurate boundary of India, including Jammu &amp; Kashmir,
        Aksai Chin, and other territories.
        As per the <strong>Government of India's guidelines</strong>, displaying
        an incorrect or incomplete map of India in any public-facing application
        is a punishable offence. A legally certified India-specific boundary
        is therefore <strong>intentionally excluded</strong> from this
        open-source dashboard to avoid any misrepresentation of Indian territory.
        </div>
        """,
        unsafe_allow_html=True,
    )
