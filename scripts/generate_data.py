"""
BlueMart Retail LLC – Synthetic Omni-Channel Retail Dataset Generator
Refactored for Industry Standards
"""

import pandas as pd
import numpy as np
import random
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# ============================================================================
# CONFIGURATION
# ============================================================================
np.random.seed(42)
random.seed(42)

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
BASE_DAILY_TRANSACTIONS = 150
QUICK_MODE = False

# ============================================================================
# 1️⃣ STORE MASTER
# ============================================================================
def generate_stores():
    print("Generating Store Master...")
    stores = pd.DataFrame({
        "store_id": range(1, 51),
        "store_name": [f"BlueMart Store {i:02d}" for i in range(1, 51)],
        "city": np.random.choice(["Dubai", "Abu Dhabi", "Sharjah"], 50, p=[0.5, 0.3, 0.2]),
        "store_type": np.random.choice(["Mall", "High Street", "Community"], 50, p=[0.4, 0.4, 0.2]),
        "opening_date": pd.date_range("2017-06-01", periods=50, freq="30D")[:50]
    })
    
    stores.loc[stores["opening_date"] > "2018-01-01", "opening_date"] = pd.date_range("2017-01-01", "2018-01-01", periods=len(stores[stores["opening_date"] > "2018-01-01"]))
    stores["opening_date"] = pd.to_datetime(stores["opening_date"])
    stores = stores.sort_values("opening_date").reset_index(drop=True)
    stores.loc[0:9, "opening_date"] = pd.date_range("2017-01-01", periods=10, freq="30D")
    
    print(f"Generated {len(stores)} stores")
    return stores

# ============================================================================
# 2️⃣ SKU MASTER
# ============================================================================
def generate_skus():
    print("Generating SKU Master...")
    categories = ["Grocery", "Beverages", "Personal Care", "Household", "Snacks", "Dairy", "Electronics"]
    subcategories = {
        "Grocery": ["Rice", "Pasta", "Cereals", "Canned Goods", "Spices"],
        "Beverages": ["Soft Drinks", "Juices", "Water", "Coffee", "Tea"],
        "Personal Care": ["Shampoo", "Soap", "Toothpaste", "Deodorant", "Skincare"],
        "Household": ["Cleaning Supplies", "Detergent", "Trash Bags", "Paper Products"],
        "Snacks": ["Chips", "Biscuits", "Chocolates", "Nuts", "Crackers"],
        "Dairy": ["Milk", "Yogurt", "Cheese", "Butter", "Cream"],
        "Electronics": ["Mobile Accessories", "Cables", "Batteries", "Chargers"]
    }
    
    sku_records = []
    for i, sku_id in enumerate(range(1001, 1201)):
        category = np.random.choice(categories)
        subcategory = np.random.choice(subcategories[category])
        
        price_ranges = {
            "Grocery": (5, 50), "Beverages": (3, 30), "Personal Care": (10, 80),
            "Household": (8, 60), "Snacks": (2, 25), "Dairy": (5, 40), "Electronics": (15, 250)
        }
        
        min_price, max_price = price_ranges[category]
        unit_price = np.round(np.random.uniform(min_price, max_price), 2)
        cost_price = np.round(unit_price * np.random.uniform(0.55, 0.80), 2)
        
        sku_records.append({
            "sku_id": sku_id,
            "sku_name": f"{category}_{subcategory}_{sku_id}",
            "category": category,
            "subcategory": subcategory,
            "unit_price": unit_price,
            "cost_price": cost_price,
            "brand": np.random.choice(["BlueMart", "Premium", "Budget", "Local", "International"], p=[0.2, 0.3, 0.2, 0.15, 0.15])
        })
    
    sku_master = pd.DataFrame(sku_records)
    print(f"Generated {len(sku_master)} SKUs")
    return sku_master

# ============================================================================
# 3️⃣ PROMOTIONS
# ============================================================================
def generate_promotions(start_date, end_date):
    print("Generating Promotions...")
    # Simplified for brevity, keeping core logic
    holidays = []
    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    
    for year in range(start_year, end_year + 1):
        # Add a few key promos
        holidays.append({"promo_name": f"Ramadan Sale {year}", "start_date": f"{year}-04-01", "end_date": f"{year}-05-01", "discount_pct": 20, "promo_type": "Ramadan"})
        holidays.append({"promo_name": f"Black Friday {year}", "start_date": f"{year}-11-25", "end_date": f"{year}-11-30", "discount_pct": 35, "promo_type": "Black Friday"})
        holidays.append({"promo_name": f"Summer Sale {year}", "start_date": f"{year}-07-01", "end_date": f"{year}-07-15", "discount_pct": 15, "promo_type": "Summer"})

    promotions_df = pd.DataFrame(holidays)
    promotions_df["promo_id"] = range(1, len(promotions_df) + 1)
    promotions_df["start_date"] = pd.to_datetime(promotions_df["start_date"])
    promotions_df["end_date"] = pd.to_datetime(promotions_df["end_date"])
    
    print(f"Generated {len(promotions_df)} promotions")
    return promotions_df

# ============================================================================
# 4️⃣ CUSTOMERS
# ============================================================================
def generate_customers():
    print("Generating Customer Master...")
    customers = pd.DataFrame({
        "cust_id": range(1, 5001),
        "age": np.random.choice([20, 30, 40, 50, 60], 5000),
        "gender": np.random.choice(["Male", "Female"], 5000),
        "city": np.random.choice(["Dubai", "Abu Dhabi", "Sharjah"], 5000),
        "loyalty_segment": np.random.choice(["Silver", "Gold", "Platinum"], 5000, p=[0.6, 0.3, 0.1]),
        "registration_date": pd.to_datetime(START_DATE)
    })
    print(f"Generated {len(customers)} customers")
    return customers

# ============================================================================
# 5️⃣ SALES TRANSACTIONS (WITH BASKET LOGIC)
# ============================================================================
def generate_sales(stores, sku_master, customers, promotions_df):
    print("Generating Sales Transactions with Basket Logic...")
    
    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    
    # Basket Logic: Define related categories
    # If you buy Pasta (Grocery), you might buy Sauce (Grocery) or Cheese (Dairy)
    # If you buy Shampoo (Personal Care), you might buy Conditioner (Personal Care)
    
    sales_data = []
    
    sku_list = sku_master["sku_id"].values
    sku_cats = dict(zip(sku_master["sku_id"], sku_master["category"]))
    sku_prices = dict(zip(sku_master["sku_id"], sku_master["unit_price"]))
    
    # Pre-compute promo dates
    promo_map = {}
    for _, row in promotions_df.iterrows():
        for d in pd.date_range(row["start_date"], row["end_date"]):
            promo_map[d] = row["discount_pct"]

    transaction_id_counter = 1
    
    # Process day by day (simplified for performance in this demo)
    # In a real scenario, we might vectorize, but basket logic is easier to read iteratively
    
    total_days = len(dates)
    print(f"   Processing {total_days} days...")
    
    # Optimization: Generate fewer days or sample if needed, but we'll do full range
    # User requested 100-150 transactions PER STORE. There are 50 stores.
    # So total daily transactions = BASE_DAILY_TRANSACTIONS * 50
    daily_tx_count = BASE_DAILY_TRANSACTIONS * 50 
    
    for current_date in dates:
        is_promo = current_date in promo_map
        num_transactions = int(daily_tx_count * (1.5 if is_promo else 1.0))
        
        # Vectorized generation for the day's transactions
        day_store_ids = np.random.choice(stores["store_id"], num_transactions)
        day_cust_ids = np.random.choice(customers["cust_id"], num_transactions)
        
        for i in range(num_transactions):
            store_id = day_store_ids[i]
            cust_id = day_cust_ids[i] if np.random.random() > 0.2 else None # 20% walk-ins
            
            # Start Basket
            basket_size = np.random.choice([1, 2, 3, 4, 5], p=[0.3, 0.3, 0.2, 0.1, 0.1])
            
            # Pick first item
            first_item = np.random.choice(sku_list)
            basket_items = [first_item]
            
            # Pick related items based on category of first item
            first_cat = sku_cats[first_item]
            
            # Simple correlation: 50% chance next item is same category
            for _ in range(basket_size - 1):
                if np.random.random() < 0.5:
                    # Same category
                    same_cat_skus = sku_master[sku_master["category"] == first_cat]["sku_id"].values
                    if len(same_cat_skus) > 0:
                        basket_items.append(np.random.choice(same_cat_skus))
                    else:
                        basket_items.append(np.random.choice(sku_list))
                else:
                    # Random other item
                    basket_items.append(np.random.choice(sku_list))
            
            # Record transactions
            for item_id in basket_items:
                price = sku_prices[item_id]
                discount = promo_map.get(current_date, 0)
                final_price = price * (1 - discount/100)
                
                sales_data.append({
                    "date": current_date,
                    "store_id": store_id,
                    "sku_id": item_id,
                    "customer_id": cust_id,
                    "quantity": np.random.randint(1, 4),
                    "unit_price": round(final_price, 2),
                    "total_value": round(final_price * np.random.randint(1, 4), 2), # simplified qty mult
                    "total_value": round(final_price * np.random.randint(1, 4), 2), # simplified qty mult
                    "channel": np.random.choice(["Store", "Website", "MobileApp", "Amazon.ae", "Noon"], p=[0.5, 0.25, 0.15, 0.07, 0.03]),
                    "discount_pct": discount,
                    "discount_pct": discount,
                    "transaction_id": transaction_id_counter
                })
            
            transaction_id_counter += 1
            
    sales = pd.DataFrame(sales_data)
    print(f"Generated {len(sales)} sales records")
    return sales

# ============================================================================
# 6️⃣ INVENTORY
# ============================================================================
def generate_inventory(stores, sku_master):
    print("Generating Inventory...")
    # Simplified inventory generation
    inventory_records = []
    for store_id in stores["store_id"]:
        # Random 100 SKUs per store
        store_skus = np.random.choice(sku_master["sku_id"], 100, replace=False)
        for sku_id in store_skus:
            inventory_records.append({
                "store_id": store_id,
                "sku_id": sku_id,
                "stock_on_hand": np.random.randint(10, 200),
                "reorder_point": 20,
                "snapshot_date": END_DATE
            })
    inventory = pd.DataFrame(inventory_records)
    print(f"Generated {len(inventory)} inventory records")
    return inventory

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print(f"Starting Data Generation... Saving to {config.RAW_DATA_DIR}")
    
    stores = generate_stores()
    skus = generate_skus()
    promos = generate_promotions(START_DATE, END_DATE)
    customers = generate_customers()
    sales = generate_sales(stores, skus, customers, promos)
    inventory = generate_inventory(stores, skus)
    
    # Save using config paths
    stores.to_csv(config.FILE_STORES, index=False)
    skus.to_csv(config.FILE_SKUS, index=False)
    promos.to_csv(config.FILE_PROMOTIONS, index=False)
    customers.to_csv(config.FILE_CUSTOMERS, index=False)
    sales.to_csv(config.FILE_SALES, index=False)
    inventory.to_csv(config.FILE_INVENTORY, index=False)
    
    print("Data Generation Complete!")
