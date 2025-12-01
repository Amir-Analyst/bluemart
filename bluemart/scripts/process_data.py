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
    
    # 1. Load Master Data (Small enough for memory)
    try:
        print("   Loading master data...")
        skus = pd.read_csv(config.FILE_SKUS)
        stores = pd.read_csv(config.FILE_STORES)
        promos = pd.read_csv(config.FILE_PROMOTIONS, parse_dates=['start_date', 'end_date'])
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        print("   Please run scripts/generate_data.py first.")
        return

    # Pre-process promos for faster lookup
    promos = promos.sort_values('start_date')
    promo_lookup = {}
    for _, row in promos.iterrows():
        for d in pd.date_range(row['start_date'], row['end_date']):
            promo_lookup[d] = row['promo_name']

    # Initialize aggregation containers
    partial_aggregates = []
    
    # Global metrics counters
    global_metrics = {
        "total_revenue": 0.0,
        "total_profit": 0.0,
        "total_quantity": 0,
        "count": 0
    }
    
    chunk_size = 50000  # Reduced from 100,000 to prevent OOM
    print(f"   Processing sales data in chunks of {chunk_size}...")
    
    try:
        # Process Sales in Chunks
        # Optimization: Read only necessary columns and specify types
        use_cols = ['date', 'store_id', 'sku_id', 'quantity', 'total_value', 'channel']
        dtype_spec = {
            'store_id': 'int32',
            'sku_id': 'int32',
            'quantity': 'int32',
            'total_value': 'float32',
            'channel': 'category'
        }
        
        chunk_iter = pd.read_csv(
            config.FILE_SALES, 
            chunksize=chunk_size, 
            usecols=use_cols, 
            dtype=dtype_spec,
            parse_dates=['date'] # Parse dates directly to avoid later conversion overhead
        )
        
        for i, chunk in enumerate(chunk_iter):
            # Data Cleaning & Type Enforcement not needed as much with dtype_spec, 
            # but good to be safe on IDs if they were somehow NaN (though int32 would fail on NaN)
            # If we have NaNs, read_csv with int32 might fail. 
            # Safe approach: Let read_csv handle it, if it fails we might need Int32 (nullable)
            # But generated data shouldn't have NaNs in IDs.
            
            # Merge
            chunk = chunk.merge(skus, on='sku_id', how='left').merge(stores, on='store_id', how='left')
            
            # Feature Engineering
            # Date is already parsed by read_csv
            # Drop rows with invalid dates
            chunk = chunk.dropna(subset=['date'])
            chunk['promo_name'] = chunk['date'].map(promo_lookup).fillna('No Promotion')
            chunk['month'] = chunk['date'].dt.month_name()
            chunk['year'] = chunk['date'].dt.year
            chunk['revenue'] = chunk['total_value']
            chunk['profit'] = chunk['revenue'] - (chunk['cost_price'] * chunk['quantity'])
            
            # Update Global Metrics
            global_metrics["total_revenue"] += chunk['revenue'].sum()
            global_metrics["total_profit"] += chunk['profit'].sum()
            global_metrics["total_quantity"] += int(chunk['quantity'].sum())
            global_metrics["count"] += len(chunk)
            
            # Partial Aggregation for Dashboard
            # Group by key dimensions to reduce size immediately
            # OPTIMIZATION: Group by IDs only to avoid string overhead and Cartesian product issues
            # We will merge names back at the very end.
            grouped_chunk = chunk.groupby(
                ['month', 'year', 'store_id', 'category', 'channel', 'sku_id'],
                observed=True # CRITICAL: Only group observed combinations, not all categoricals
            ).agg(
                revenue=('revenue', 'sum'),
                profit=('profit', 'sum'),
                quantity=('quantity', 'sum')
            ).reset_index()
            
            partial_aggregates.append(grouped_chunk)
            
            # OPTIMIZATION: Iterative Aggregation
            # Instead of accumulating thousands of DataFrames in partial_aggregates,
            # we merge them into a main accumulator every few chunks to keep memory usage low.
            if len(partial_aggregates) >= 10:
                print("   Compacting partial aggregates...")
                temp_df = pd.concat(partial_aggregates)
                
                # Group again to reduce size
                temp_df = temp_df.groupby(
                    ['month', 'year', 'store_id', 'category', 'channel', 'sku_id'],
                    observed=True
                ).agg(
                    revenue=('revenue', 'sum'),
                    profit=('profit', 'sum'),
                    quantity=('quantity', 'sum')
                ).reset_index()
                
                # If we already have a main accumulator, merge with it
                if 'dashboard_df' in locals():
                    dashboard_df = pd.concat([dashboard_df, temp_df])
                    dashboard_df = dashboard_df.groupby(
                        ['month', 'year', 'store_id', 'category', 'channel', 'sku_id'],
                        observed=True
                    ).agg(
                        revenue=('revenue', 'sum'),
                        profit=('profit', 'sum'),
                        quantity=('quantity', 'sum')
                    ).reset_index()
                else:
                    dashboard_df = temp_df
                
                # Clear the list to free memory
                partial_aggregates = []
                import gc
                gc.collect()
            
            if (i + 1) % 5 == 0:
                print(f"   Processed {i + 1} chunks...")
                import gc
                gc.collect()
                
    except FileNotFoundError:
         print(f"Error: {config.FILE_SALES} not found.")
         return

    # 4. Final Aggregation
    print("   Performing final aggregation...")
    
    # Process any remaining chunks in partial_aggregates
    if partial_aggregates:
        temp_df = pd.concat(partial_aggregates)
        if 'dashboard_df' in locals():
            dashboard_df = pd.concat([dashboard_df, temp_df])
        else:
            dashboard_df = temp_df
            
    if 'dashboard_df' not in locals() or dashboard_df.empty:
        print("No data processed.")
        return

    # Final Groupby to ensure uniqueness
    dashboard_df = dashboard_df.groupby(
        ['month', 'year', 'store_id', 'category', 'channel', 'sku_id'],
        observed=True
    ).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    # Merge names back
    print("   Merging names back...")
    # We need to reload masters briefly or keep them in memory (they are small)
    # skus and stores are already in memory from start of script
    dashboard_df = dashboard_df.merge(skus[['sku_id', 'sku_name']], on='sku_id', how='left')
    dashboard_df = dashboard_df.merge(stores[['store_id', 'store_name']], on='store_id', how='left')

    # DEBUG: Print monthly revenue to verify Ramadan (April) sales
    print("\n   [DEBUG] Monthly Revenue Check:")
    monthly_check = dashboard_df.groupby('month')['revenue'].sum().sort_values(ascending=False)
    print(monthly_check)
    print("   -----------------------------\n")
    
    # 5. Save Summary Metrics
    print("   Calculating final global metrics...")
    summary_metrics = {
        "total_revenue": float(global_metrics["total_revenue"]),
        "total_profit": float(global_metrics["total_profit"]),
        "total_quantity": int(global_metrics["total_quantity"]),
        "avg_revenue_per_order": float(global_metrics["total_revenue"] / global_metrics["count"]) if global_metrics["count"] > 0 else 0,
        "avg_profit_per_order": float(global_metrics["total_profit"] / global_metrics["count"]) if global_metrics["count"] > 0 else 0
    }
    
    import json
    print(f"Saving summary metrics to {config.FILE_SUMMARY_METRICS}")
    with open(config.FILE_SUMMARY_METRICS, 'w') as f:
        json.dump(summary_metrics, f)
    
    # 6. Save Dashboard Data
    print(f"Saving processed data to {config.FILE_DASHBOARD_DATA}")
    dashboard_df.to_csv(config.FILE_DASHBOARD_DATA, index=False)
    print("Data Processing Complete!")

if __name__ == "__main__":
    process_data()
