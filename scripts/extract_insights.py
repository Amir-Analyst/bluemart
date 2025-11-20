import pandas as pd
import json

# Load data
df = pd.read_csv('data/processed/sales_dashboard_data.csv')

# Category performance
cat = df.groupby('category').agg({'revenue': 'sum', 'profit': 'sum', 'quantity': 'sum'}).sort_values('revenue', ascending=False)
cat['margin_pct'] = (cat['profit'] / cat['revenue'] * 100).round(1)
cat['revenue_share'] = (cat['revenue'] / cat['revenue'].sum() * 100).round(1)

print("=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)
print(cat.to_string())

# Channel distribution
print("\n" + "=" * 60)
print("CHANNEL DISTRIBUTION")
print("=" * 60)
ch = df.groupby('channel')['revenue'].sum().sort_values(ascending=False)
ch_pct = (ch / ch.sum() * 100).round(1)
for channel, pct in ch_pct.items():
    print(f"{channel:15s}: {pct:5.1f}% (AED {ch[channel]/1e6:,.1f}M)")

# Store performance by city
print("\n" + "=" * 60)
print("CITY PERFORMANCE")
print("=" * 60)
stores_df = pd.read_csv('data/raw/bm_stores.csv')
store_perf = df.groupby('store_id')['revenue'].sum().reset_index()
store_perf = store_perf.merge(stores_df[['store_id', 'city']], on='store_id')
city_perf = store_perf.groupby('city')['revenue'].sum().sort_values(ascending=False)
city_pct = (city_perf / city_perf.sum() * 100).round(1)
for city, pct in city_pct.items():
    print(f"{city:15s}: {pct:5.1f}% (AED {city_perf[city]/1e6:,.1f}M)")

# Monthly trends
print("\n" + "=" * 60)
print("TOP 3 REVENUE MONTHS")
print("=" * 60)
monthly = df.groupby('month')['revenue'].sum().sort_values(ascending=False).head(3)
for month, rev in monthly.items():
    print(f"{month:15s}: AED {rev/1e6:,.1f}M")

# Top SKUs
print("\n" + "=" * 60)
print("TOP 10 SKUs BY REVENUE")
print("=" * 60)
top_skus = df.groupby(['sku_id', 'sku_name'])['revenue'].sum().sort_values(ascending=False).head(10)
for (sku_id, sku_name), rev in top_skus.items():
    print(f"{sku_name[:40]:40s}: AED {rev/1e6:,.2f}M")

print("\n" + "=" * 60)
print("SUMMARY METRICS")
print("=" * 60)
with open('data/processed/summary_metrics.json', 'r') as f:
    metrics = json.load(f)
print(f"Total Revenue:     AED {metrics['total_revenue']/1e6:,.1f}M")
print(f"Total Profit:      AED {metrics['total_profit']/1e6:,.1f}M")
print(f"Gross Margin:      {metrics['total_profit']/metrics['total_revenue']*100:.1f}%")
print(f"Total Units Sold:  {metrics['total_quantity']/1e6:,.1f}M")
print(f"Avg Order Value:   AED {metrics['avg_revenue_per_order']:.2f}")
print(f"Avg Order Profit:  AED {metrics['avg_profit_per_order']:.2f}")
