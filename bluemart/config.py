import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# File paths - Raw
FILE_STORES = RAW_DATA_DIR / "bm_stores.csv"
FILE_SKUS = RAW_DATA_DIR / "bm_skus.csv"
FILE_SALES = RAW_DATA_DIR / "bm_sales.csv"
FILE_PROMOTIONS = RAW_DATA_DIR / "bm_promotions.csv"
FILE_CUSTOMERS = RAW_DATA_DIR / "bm_customers.csv"
FILE_INVENTORY = RAW_DATA_DIR / "bm_inventory.csv"

# File paths - Processed
FILE_DASHBOARD_DATA = PROCESSED_DATA_DIR / "sales_dashboard_data.csv"
FILE_SUMMARY_METRICS = PROCESSED_DATA_DIR / "summary_metrics.json"
