import pandas as pd
import numpy as np
import os

# Configuration
COUNTRIES = {
    "South Asia": ["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "Bhutan"],
    "South East Asia": [
        "Indonesia",
        "Viet Nam",
        "Thailand",
        "Myanmar",
        "Malaysia",
        "Philippines",
        "Singapore",
    ],
}

INDICATORS = {
    "SDG 2": [
        "Prevalence of Undernourishment (%)",
        "Stunting in Children < 5 Years (%)",
    ],
    "SDG 3": [
        "Maternal Mortality Ratio (per 100k births)",
        "Under-5 Mortality Rate (per 1,000 live births)",
    ],
    "SDG 6": ["Safely Managed Drinking Water (%)", "Open Defecation Practice (%)"],
}


def generate_data():
    np.random.seed(42)
    records = []
    years = range(2000, 2025)

    for region, country_list in COUNTRIES.items():
        for country in country_list:
            # Add some country-specific bias
            country_bias = np.random.uniform(-10, 10)
            if country == "India":
                country_bias = 0  # Baseline
            elif country == "Singapore":
                country_bias = 40  # High performer bias

            for sdg, inds in INDICATORS.items():
                for ind in inds:
                    # Determine base value and trend direction
                    if (
                        "Mortality" in ind
                        or "Stunting" in ind
                        or "Undernourishment" in ind
                        or "Defecation" in ind
                    ):
                        # Negative indicators (lower is better)
                        base_val = 50 + country_bias
                        trend = -0.8  # Improving over time
                    else:
                        # Positive indicators (higher is better)
                        base_val = 60 + country_bias
                        trend = 0.8  # Improving over time

                    current_val = max(0, min(100, base_val))

                    for i, year in enumerate(years):
                        # Add trend and noise
                        noise = np.random.normal(0, 1.5)
                        val = current_val + (trend * i) + noise

                        # Clamp values
                        val = max(0, min(100, val))

                        records.append(
                            {
                                "GeoAreaName": country,
                                "TimePeriod": year,
                                "Indicator": ind,
                                "Value": round(val, 2),
                                "SDG": sdg,
                                "Region": region,
                            }
                        )

    df = pd.DataFrame(records)

    # Save to the specific path the app expects (root of the workspace or data folder)
    # The app code expects "final_sdg_data.csv" in the current directory.
    output_path = os.path.join(os.path.dirname(__file__), "..", "final_sdg_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Data generated at {output_path}")
    print(df.head())


if __name__ == "__main__":
    generate_data()
