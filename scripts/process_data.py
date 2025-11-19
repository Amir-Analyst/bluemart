"""
BlueMart Data Processing Pipeline
Refactored for Industry Standards
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def process_data():
    print("Starting Data Processing...")
    
    # 1. Load Data
    try:
        print("   Loading raw data...")
        sales = pd.read_csv(config.FILE_SALES, parse_dates=['date'])
        skus = pd.read_csv(config.FILE_SKUS)
        stores = pd.read_csv(config.FILE_STORES)
        promos = pd.read_csv(config.FILE_PROMOTIONS, parse_dates=['start_date', 'end_date'])
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        print("   Please run scripts/generate_data.py first.")
        return

    # 2. Merge Data
    print("   Merging datasets...")
    # Merge Sales + SKU + Store
    df = sales.merge(skus, on='sku_id', how='left').merge(stores, on='store_id', how='left')
    
    # 3. Optimize Promotion Matching (Vectorized approach using merge_asof if sorted, or simple join if ranges don't overlap much)
    # For simplicity and robustness with ranges, we'll keep it simple but ensure it's efficient.
    # Since we already have discount_pct in sales from generator, we might not need to re-match!
    # But let's assume we need to enrich with promo NAME.
    
    # Sort for merge_asof
    df = df.sort_values('date')
    promos = promos.sort_values('start_date')
    
    # A simple approach for promo names:
    # Create a daily promo lookup
    promo_lookup = {}
    for _, row in promos.iterrows():
        for d in pd.date_range(row['start_date'], row['end_date']):
            promo_lookup[d] = row['promo_name']
            
    df['promo_name'] = df['date'].map(promo_lookup).fillna('No Promotion')
    
    # 4. Feature Engineering
    print("   Calculating metrics...")
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['revenue'] = df['total_value']
    df['profit'] = df['revenue'] - (df['cost_price'] * df['quantity'])

    # 4.5 Calculate Global Summary Metrics (Pre-aggregation)
    print("   Calculating global summary metrics...")
    summary_metrics = {
        "total_revenue": float(df['revenue'].sum()),
        "total_profit": float(df['profit'].sum()),
        "total_quantity": int(df['quantity'].sum()),
        "avg_revenue_per_order": float(df['revenue'].mean()),
        "avg_profit_per_order": float(df['profit'].mean())
    }
    
    import json
    print(f"Saving summary metrics to {config.FILE_SUMMARY_METRICS}")
    with open(config.FILE_SUMMARY_METRICS, 'w') as f:
        json.dump(summary_metrics, f)
    
    # 5. Aggregation for Dashboard (Reduce file size)
    print("   Aggregating for dashboard...")
    # Group by key dimensions to make the dashboard fast
    dashboard_df = df.groupby(
        ['date', 'month', 'year', 'store_id', 'store_name', 'category', 'channel', 'sku_id', 'sku_name']
    ).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    
    # 6. Save
    print(f"Saving processed data to {config.FILE_DASHBOARD_DATA}")
    dashboard_df.to_csv(config.FILE_DASHBOARD_DATA, index=False)
    print("Data Processing Complete!")

if __name__ == "__main__":
    process_data()
