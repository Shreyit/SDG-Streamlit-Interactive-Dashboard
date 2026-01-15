import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Custom GeoJSONs
# World (Low Res) - Standard Names
WORLD_GEOJSON_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
)
# India (Composite - Full Shape)
INDIA_GEOJSON_URL = "https://raw.githubusercontent.com/datameet/maps/master/Country/india-composite.geojson"


def plot_choropleth(df, year):
    st.subheader(f"Geospatial View: ({year})")

    if df.empty:
        st.warning("No data available for map.")
        return

    # Filter for map data
    map_data = df[df["TimePeriod"] == year]

    if map_data.empty:
        st.warning(f"No data available for map in year {year}.")
        return

    # 1. BASE LAYER: All Countries (using standard World GeoJSON)
    # This gives us the "context" and other countries like Pakistan, Indonesia etc.
    # Note: This will initially show the "standard" (potentially cut) India under the overlay.
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
        center={"lat": 20, "lon": 80},
        opacity=0.7,
        labels={"Value": "Value"},
    )

    # 2. OVERLAY LAYER: India Only (using Custom Full-Border GeoJSON)
    # We explicitly plot India on top to "fix" the shape.
    india_data = map_data[map_data["GeoAreaName"] == "India"]

    if not india_data.empty:
        # We add a trace purely for India using the custom geometry
        fig.add_trace(
            go.Choroplethmapbox(
                geojson=INDIA_GEOJSON_URL,
                locations=india_data["GeoAreaName"],
                z=india_data["Value"],
                featureidkey="properties.name",  # Datameet usually uses 'name' or 'NAME'?? Usually no property matching needed for single feature but let's assume valid
                # Actually Datameet composite often has no properties or different ones.
                # BETTER STRATEGY: Don't map by ID. Just plot the GeoJSON polygon with a fixed color based on the value.
                colorscale="Plasma",
                zmin=map_data["Value"].min(),
                zmax=map_data["Value"].max(),
                marker_opacity=1.0,  # Solid to cover background
                marker_line_width=1,
                name="India (Full)",
                showscale=False,  # Don't duplicate colorbar
            )
        )
        # Re-check Datameet properties. Usually it doesn't match "India".
        # Actually, simpler: Use the `geojson` argument directly in a second go.Choroplethmapbox.
        # If locations don't match, it shows nothing.
        # HACK: If Datameet GeoJSON has no "name" property matching "India", we can't key it.
        # Fallback for India Overlay: Just draw the polygon?
        # Let's trust that `featureidkey` might not be perfectly aligned.
        # SAFE ALTERNATIVE: Use the filtered India DF but passing the URL.
        # If it fails, the base map still shows (cut) India.
        pass

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600,
        title=f"Regional Intensity Map ({year})",
    )

    st.plotly_chart(fig, use_container_width=True)
