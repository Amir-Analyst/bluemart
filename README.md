# BlueMart Retail Analytics Project

This project simulates a retail analytics environment for BlueMart, a UAE-based omnichannel retailer. It demonstrates data generation, processing, and visualization using Python and Streamlit.

## 📂 Project Structure

```text
bluemart/
├── config.py                 # Central configuration for paths
├── requirements.txt          # Project dependencies
├── app.py                    # Streamlit Dashboard
├── scripts/                  # Data pipeline scripts
│   ├── generate_data.py      # Generates synthetic data with basket logic
│   └── process_data.py       # Processes raw data for the dashboard
└── data/                     # Data storage (gitignored)
    ├── raw/                  # Generated raw CSVs
    └── processed/            # Optimized data for the dashboard
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Data
Run the data generator to create synthetic transaction data. This script includes logic for seasonality, store types, and "basket" purchasing behavior.
```bash
python scripts/generate_data.py
```
*Output: CSV files in `data/raw/`*

### 3. Process Data
Run the processing script to clean, merge, and aggregate the data for the dashboard.
```bash
python scripts/process_data.py
```
*Output: `sales_dashboard_data.csv` in `data/processed/`*

### 4. Run Dashboard
Launch the interactive Streamlit dashboard.
```bash
streamlit run app.py
```

## 📊 Features
- **Synthetic Data Generator**: Creates realistic retail data including customers, stores, SKUs, and transactions with basket correlation.
- **Data Pipeline**: Modular scripts for ETL (Extract, Transform, Load) operations.
- **Interactive Dashboard**: Visualizes key metrics like Revenue, Profit, and Category performance.

## 🛠 Technologies
- Python
- Pandas & NumPy
- Streamlit
- Plotly

## 📝 License
For educational purposes.
