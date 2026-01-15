# SDG Command Center: South & Southeast Asia Analysis

A high-fidelity interactive dashboard for analyzing Sustainable Development Goals (SDG 2, 3, 6) across South and Southeast Asia, with a specific focus on India. Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).

## 🚀 Features
*   **Dynamic Theming**: UI colors adapt automatically based on the selected SDG (Yellow for SDG 2, Green for SDG 3, Blue for SDG 6).
*   **Interactive Maps**: Dual-layer geospatial view with "Carto-Positron" tiles and a custom overlay for **India's full borders** (including J&K).
*   **Comparative Analytics**: Trend analysis, Peer Comparison (India vs Top 5), and a multi-variant Radar Chart.
*   **High-Quality Visualization**: Crisp, sharp custom icons and responsive charts.
*   **Methods & References**: Dedicated tab explaining indicators and data sources (UN SDG Database, World Bank, Datameet).

## 📊 Data Indicators
*   **SDG 2 (Zero Hunger)**: Undernourishment (2.1.1), Stunting (2.2.1)
*   **SDG 3 (Good Health)**: Maternal Mortality (3.1.1), Under-5 Mortality (3.2.1)
*   **SDG 6 (Clean Water)**: Safely managed Drinking Water (6.1.1) & Sanitation (6.2.1)

## 🛠️ Installation & Running Locally

1.  **Clone the repository** (or download the folder):
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    streamlit run main.py
    ```

## ☁️ Deployment Guide

### Option 1: Deploy to Streamlit Community Cloud (Free)
This is the easiest way to share your app.

1.  **Push to GitHub**:
    *   Create a new repository on [GitHub](https://github.com/).
    *   Upload all files from this folder (`appSDG/`) to the repository.
    *   Ensure `requirements.txt` is in the root of your repository.

2.  **Deploy**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Click **"New app"**.
    *   Select your GitHub repository, branch (usually `main`), and the main file path (`main.py`).
    *   Click **"Deploy"**.

### Option 2: Deploy to Data Button / Hugging Face Spaces
*   **Hugging Face**: Create a new Space, select "Streamlit" as the SDK, and upload your files (including `requirements.txt`).

## 📁 Project Structure
```text
.
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── data_loader.py          # Data processing logic
├── utils_constants.py      # Mappings and configuration
├── SDG_final.csv           # Source data (processed)
├── components/
│   ├── charts.py           # Plotly chart definitions
│   └── map.py              # Map visualization logic
└── assets/                 # Icons and images
```

## 📝 Credits
*   **Data Sources**: UN SDG Indicators Database, World Bank, DataMeet (India Boundaries).
*   **Icons**: Official SDG Icons (UN Communications Guidelines).
