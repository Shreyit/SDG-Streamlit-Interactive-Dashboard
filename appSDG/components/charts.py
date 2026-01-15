import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from utils import get_sdg_colors


def plot_trend_line(df, indicator, selected_sdg):
    st.subheader("1. Regional Trajectory")

    # Validation
    if df.empty:
        st.warning("No data for trend analysis.")
        return

    # Get Theme Colors
    theme = get_sdg_colors(selected_sdg)
    main_color = theme["main"]

    # Plot
    fig_trend = px.line(
        df,
        x="TimePeriod",
        y="Value",
        color="GeoAreaName",
        color_discrete_map={"India": main_color},  # Use Theme Main Color for India
        title=f"{indicator}: Trend over Time",
        hover_data=["Value"],
    )

    # Make non-India lines thinner/transparent (but visible)
    fig_trend.update_traces(line=dict(width=3.0), opacity=0.7)
    # Make India thick and solid
    fig_trend.update_traces(
        selector=dict(name="India"), line=dict(width=4, color=main_color), opacity=1.0
    )

    st.plotly_chart(fig_trend, use_container_width=True)


def plot_peer_comparison(df, latest_year, selected_sdg):  # Added selected_sdg arg
    st.subheader("2. Peer Comparison (Latest Year)")

    if df.empty:
        st.warning("No data for peer comparison.")
        return

    # Get Theme Colors
    theme = get_sdg_colors(selected_sdg)
    main_color = theme["main"]
    light_color = theme["light"]

    bar_data = df[df["TimePeriod"] == latest_year].sort_values("Value", ascending=True)

    # Color logic: Highlight India with Theme Color, Peers with light distinct color
    bar_colors = [
        main_color if x == "India" else light_color for x in bar_data["GeoAreaName"]
    ]

    fig_bar = go.Figure(
        data=[
            go.Bar(
                x=bar_data["GeoAreaName"], y=bar_data["Value"], marker_color=bar_colors
            )
        ]
    )
    fig_bar.update_layout(title=f"Standing in {latest_year}")
    st.plotly_chart(fig_bar, use_container_width=True)


def plot_radar_chart(
    df, latest_year, sdg_map, selected_region, selected_countries, selected_sdg
):
    st.subheader("3. Comprehensive SDG Performance (Goals 2, 3, 6)")

    # Get Theme Colors
    theme = get_sdg_colors(selected_sdg)
    main_color = theme["main"]

    # 1. Gather ALL relevant indicators (ordered by SDG)
    # We flatten the map to get a single list of indicators in order
    all_indicators = []

    # Explicit order for coloring sectors
    sdg_order = ["SDG 2", "SDG 3", "SDG 6"]
    for sdg in sdg_order:
        if sdg in sdg_map:
            all_indicators.extend(sdg_map[sdg])

    # Filter for relevant data (All countries, latest year)
    radar_base_df = df[
        (df["Indicator"].isin(all_indicators)) & (df["TimePeriod"] == latest_year)
    ]

    if radar_base_df.empty:
        st.warning("Insufficient data for Radar Chart.")
        return

    # Pivot all data
    pivot_all = radar_base_df.pivot_table(
        index="GeoAreaName", columns="Indicator", values="Value", aggfunc="mean"
    )

    if pivot_all.empty:
        st.warning("No pivot data for Radar.")
        return

    # --- IMPROVED NORMALIZATION: Context-Aware ---
    relevant_countries = set(selected_countries)
    relevant_countries.add("India")
    if selected_region in ["All", "South Asia"]:
        relevant_countries.update(
            df[df["Region"] == "South Asia"]["GeoAreaName"].unique()
        )
    if selected_region in ["All", "South East Asia"]:
        relevant_countries.update(
            df[df["Region"] == "South East Asia"]["GeoAreaName"].unique()
        )

    scaling_df = radar_base_df[radar_base_df["GeoAreaName"].isin(relevant_countries)]
    if scaling_df.empty:
        scaling_df = radar_base_df

    pivot_scaling = scaling_df.pivot_table(
        index="GeoAreaName", columns="Indicator", values="Value", aggfunc="mean"
    )

    local_min = pivot_scaling.min()
    local_max = pivot_scaling.max()
    diff = local_max - local_min
    diff[diff == 0] = 1

    def get_norm_values(series):
        # Handle missing columns safely
        valid_cols = [c for c in all_indicators if c in pivot_all.columns]
        # Align series to these cols
        s = series.reindex(valid_cols)
        m = local_min.reindex(valid_cols)
        d = diff.reindex(valid_cols)
        return ((s - m) / d).fillna(0).tolist()  # FillNA 0 for safety

    # Ensure categories match the order of 'all_indicators' present in data
    categories = [c for c in all_indicators if c in pivot_all.columns]

    fig_radar = go.Figure()

    # --- 1. Regional Averages ---
    if selected_region in ["All", "South Asia"]:
        sa_countries = radar_base_df[radar_base_df["Region"] == "South Asia"]
        if not sa_countries.empty:
            sa_avg = sa_countries.pivot_table(
                columns="Indicator", values="Value", aggfunc="mean"
            ).iloc[0]
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=get_norm_values(sa_avg),
                    theta=categories,
                    fill="toself",
                    name="South Asia Avg",
                    line_color="orange",
                    opacity=0.3,
                    line_dash="dash",
                )
            )

    if selected_region in ["All", "South East Asia"]:
        sea_countries = radar_base_df[radar_base_df["Region"] == "South East Asia"]
        if not sea_countries.empty:
            sea_avg = sea_countries.pivot_table(
                columns="Indicator", values="Value", aggfunc="mean"
            ).iloc[0]
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=get_norm_values(sea_avg),
                    theta=categories,
                    fill="toself",
                    name="SE Asia Avg",
                    line_color="teal",
                    opacity=0.3,
                    line_dash="dash",
                )
            )

    # --- 2. Focus Country (India) ---
    if "India" in pivot_all.index:
        fig_radar.add_trace(
            go.Scatterpolar(
                r=get_norm_values(pivot_all.loc["India"]),
                theta=categories,
                fill="toself",
                name="India",
                line_color=main_color,
                opacity=0.8,
                line_width=3,  # Use Theme Color
            )
        )

    # --- 3. Peers ---
    for country in selected_countries:
        if country != "India" and country in pivot_all.index:
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=get_norm_values(pivot_all.loc[country]),
                    theta=categories,
                    fill="none",
                    name=country,
                    line_width=1,
                )
            )

    # Layout with simplified multi-color background attempt via layout.polar.bgcolor?
    # No, that's single color. We rely on grouping logic.

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.05]),
            angularaxis=dict(direction="clockwise"),
        ),
        showlegend=True,
        title="Cross-Goal Performance Analysis (SDG 2, 3, 6)",
        height=600,
        margin=dict(t=50, b=50, l=100, r=100),  # Extra margin for long labels
    )
    st.plotly_chart(fig_radar, use_container_width=True)
