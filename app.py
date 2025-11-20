# ================================================================
# 📊 BLUEMART DASHBOARD — STREAMLIT SAMPLE DATA WITH FULL STYLE
# Author: Amir
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import config

# -------------------------------
# 1️⃣ Streamlit Page Config & Theme
# -------------------------------
st.set_page_config(
    page_title="BlueMart Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Bluemart color palette - optimized for both light and dark modes
COLOR_PRIMARY = "#005f73"
COLOR_ACCENT = "#0a9396"
COLOR_SOFT = "#2ec4b6"  # Changed to vibrant teal for better dark mode visibility
COLOR_BG = "#ffffff"
CARD_BG = "#f6fbfb"

# Custom CSS for KPI cards & layout
st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {COLOR_BG}; }}
        .card {{
            background: {CARD_BG};
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 12px;
        }}
        .kpi-value {{ font-size: 24px; font-weight: 700; color: {COLOR_PRIMARY}; }}
        .kpi-label {{ font-size: 12px; color: #334155; }}
        .small-muted {{ font-size: 12px; color: #6b7280; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 2️⃣ Load Dataset with Memory Optimization
# -------------------------------
@st.cache_data
def load_data():
    """
    Load dashboard data with optimized memory usage.
    Uses efficient dtypes and chunked processing for large datasets.
    """
    try:
        # Define optimized data types to reduce memory footprint
        dtype_spec = {
            'month': 'category',
            'year': 'int16',
            'store_id': 'category',
            'store_name': 'category',
            'category': 'category',
            'channel': 'category',
            'sku_id': 'category',
            'sku_name': 'category',
            'revenue': 'float32',
            'profit': 'float32',
            'quantity': 'float32'
        }
        
        # Load data in chunks to avoid memory spike
        chunks = []
        chunk_size = 500000  # Process 500k rows at a time
        
        for chunk in pd.read_csv(
            config.FILE_DASHBOARD_DATA,
            dtype=dtype_spec,
            chunksize=chunk_size
        ):
            chunks.append(chunk)
        
        # Concatenate all chunks
        df = pd.concat(chunks, ignore_index=True)
        
        # Log memory usage for monitoring
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        print(f"[OK] Dataset loaded: {len(df):,} rows, {memory_mb:.1f} MB in memory")
        
        return df
        
    except FileNotFoundError:
        return None
    except MemoryError as e:
        st.error(f"❌ Memory error loading data: {e}")
        st.info("💡 Try reducing the dataset size or use data aggregation in process_data.py")
        return None

df = load_data()

if df is None:
    st.error("❌ Data file not found. Please run `python scripts/generate_data.py` and `python scripts/process_data.py` first.")
    st.stop()

st.sidebar.success(f"Dataset loaded: {df.shape[0]:,} rows")

# -------------------------------
# 3️⃣ Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")
store_filter = st.sidebar.multiselect("Select Store(s)", options=df['store_id'].unique(), default=df['store_id'].unique())
category_filter = st.sidebar.multiselect("Select Category(ies)", options=df['category'].unique(), default=df['category'].unique())
channel_filter = st.sidebar.multiselect("Select Channel(s)", options=df['channel'].unique(), default=df['channel'].unique())
month_filter = st.sidebar.multiselect("Select Month(s)", options=sorted(df['month'].unique()), default=sorted(df['month'].unique()))

# Apply filters
df_filtered = df[
    (df['store_id'].isin(store_filter)) &
    (df['category'].isin(category_filter)) &
    (df['channel'].isin(channel_filter)) &
    (df['month'].isin(month_filter))
]

if df_filtered.shape[0] == 0:
    st.warning("No data matches the selected filters. Try widening filters or date range.")
    st.stop()

# -------------------------------
# 4️⃣ KPI Cards
# -------------------------------
def human_format(num):
    num = float(num)
    units = ['', 'K', 'M', 'B', 'T']
    magnitude = 0
    while abs(num) >= 1000 and magnitude < len(units)-1:
        magnitude += 1
        num /= 1000.0
    if magnitude == 0:
        return f"{num:,.0f}"
    return f"{num:.1f}{units[magnitude]}"

# Load summary metrics if available
import json
summary_metrics = None
try:
    with open(config.FILE_SUMMARY_METRICS, 'r') as f:
        summary_metrics = json.load(f)
except FileNotFoundError:
    pass

# Determine metrics source
# If filters are active (subset of data), calculate from filtered DF
# If NO filters are active (full dataset view), use pre-calculated globals for speed/accuracy
is_filtered = (
    len(store_filter) < len(df['store_id'].unique()) or
    len(category_filter) < len(df['category'].unique()) or
    len(channel_filter) < len(df['channel'].unique()) or
    len(month_filter) < len(df['month'].unique())
)

if not is_filtered and summary_metrics:
    total_revenue = summary_metrics['total_revenue']
    total_profit = summary_metrics['total_profit']
    total_quantity = summary_metrics['total_quantity']
    avg_revenue = summary_metrics['avg_revenue_per_order']
    avg_profit = summary_metrics['avg_profit_per_order']
else:
    total_revenue = df_filtered['revenue'].sum()
    total_profit = df_filtered['profit'].sum()
    total_quantity = df_filtered['quantity'].sum()
    # Avg per order is tricky with aggregated data, approximation:
    avg_revenue = df_filtered['revenue'].mean() 
    avg_profit = df_filtered['profit'].mean()

col1, col2, col3, col4, col5 = st.columns(5, gap="large")
col1.markdown(f'<div class="card"><div class="small-muted">Total Revenue</div><div class="kpi-value">AED {human_format(total_revenue)}</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><div class="small-muted">Total Profit</div><div class="kpi-value">AED {human_format(total_profit)}</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><div class="small-muted">Total Quantity Sold</div><div class="kpi-value">{human_format(total_quantity)}</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="card"><div class="small-muted">Avg Revenue/Order</div><div class="kpi-value">AED {avg_revenue:,.2f}</div></div>', unsafe_allow_html=True)
col5.markdown(f'<div class="card"><div class="small-muted">Avg Profit/Order</div><div class="kpi-value">AED {avg_profit:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# 5️⃣ Top 10 SKUs by Revenue
# -------------------------------
top_skus = (
    df_filtered.groupby(['sku_id', 'sku_name'])
    .agg(revenue=('revenue', 'sum'))
    .sort_values('revenue', ascending=False)
    .head(10)
    .reset_index()
)
top_skus['revenue_formatted'] = top_skus['revenue'].map("AED {:,.2f}".format)

st.subheader("🏆 Top 10 SKUs by Revenue")
st.dataframe(top_skus[['sku_id', 'sku_name', 'revenue_formatted']], use_container_width=True)

# -------------------------------
# 6️⃣ Top 10 Stores by Revenue
# -------------------------------
top_stores = (
    df_filtered.groupby(['store_id', 'store_name'])
    .agg(revenue=('revenue', 'sum'), profit=('profit', 'sum'))
    .sort_values('revenue', ascending=False)
    .head(10)
    .reset_index()
)
top_stores['revenue'] = top_stores['revenue'].map("AED {:,.2f}".format)
top_stores['profit'] = top_stores['profit'].map("AED {:,.2f}".format)

st.subheader("🏬 Top 10 Stores by Revenue")
st.dataframe(top_stores, use_container_width=True)

# -------------------------------
# 7️⃣ Revenue by Category (Horizontal Bar)
# -------------------------------
rev_category = df_filtered.groupby('category').agg(revenue=('revenue','sum')).reset_index().sort_values('revenue', ascending=True)
fig_category = px.bar(
    rev_category, y='category', x='revenue', orientation='h',
    text='revenue', labels={'revenue':'Revenue (AED)', 'category':'Category'},
    title="📊 Revenue by Product Category", color='revenue', color_continuous_scale=[COLOR_SOFT, COLOR_PRIMARY]
)
fig_category.update_traces(texttemplate="AED %{text:.2s}", textposition='outside')
fig_category.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_category, use_container_width=True)

# -------------------------------
# 8️⃣ Revenue by Channel (Pie Chart)
# -------------------------------
st.subheader("📱 Channel Performance Analysis")
col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    rev_channel = df_filtered.groupby('channel').agg(revenue=('revenue','sum')).reset_index()
    fig_channel = px.pie(rev_channel, names='channel', values='revenue', title="Revenue Distribution by Channel",
                         color_discrete_sequence=px.colors.sequential.Teal, hole=0.4)
    fig_channel.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_channel, use_container_width=True)

with col_ch2:
    # Channel revenue table with percentages
    rev_channel['percentage'] = (rev_channel['revenue'] / rev_channel['revenue'].sum() * 100).round(1)
    rev_channel['revenue_formatted'] = rev_channel['revenue'].apply(lambda x: f"AED {human_format(x)}")
    rev_channel['percentage_formatted'] = rev_channel['percentage'].apply(lambda x: f"{x}%")
    rev_channel_display = rev_channel[['channel', 'revenue_formatted', 'percentage_formatted']].sort_values('percentage_formatted', ascending=False)
    rev_channel_display.columns = ['Channel', 'Revenue', 'Share']
    st.markdown("#### Channel Revenue Breakdown")
    st.dataframe(rev_channel_display, use_container_width=True, hide_index=True)

# -------------------------------
# 9️⃣ Gross Margin by Category
# -------------------------------
st.subheader("💰 Profitability Analysis - Margin by Category")
margin_category = df_filtered.groupby('category').agg(revenue=('revenue','sum'), profit=('profit','sum')).reset_index()
margin_category['margin_pct'] = (margin_category['profit'] / margin_category['revenue'] * 100).round(2)
margin_category = margin_category.sort_values('margin_pct', ascending=True)

# Color code based on margin health
def margin_color(margin):
    if margin >= 35:
        return '#28a745'  # Green - Excellent
    elif margin >= 30:
        return '#ffc107'  # Yellow - Good
    else:
        return '#fd7e14'  # Orange - Moderate

margin_category['color'] = margin_category['margin_pct'].apply(margin_color)

fig_margin = go.Figure(go.Bar(
    y=margin_category['category'],
    x=margin_category['margin_pct'],
    orientation='h',
    marker=dict(color=margin_category['color']),
    text=margin_category['margin_pct'].apply(lambda x: f"{x:.1f}%"),
    textposition='outside'
))
fig_margin.update_layout(
    title='Gross Margin % by Category',
    xaxis_title='Gross Margin (%)',
    yaxis_title='Category',
    showlegend=False,
    height=400,
    xaxis=dict(range=[0, max(margin_category['margin_pct']) + 5])
)
st.plotly_chart(fig_margin, use_container_width=True)

# Margin legend
st.markdown("""
<div style='display: flex; gap: 20px; font-size: 12px; margin-top: -10px;'>
    <span>🟢 Excellent (≥35%)</span>
    <span>🟡 Good (30-35%)</span>
    <span>🟠 Moderate (<30%)</span>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# 🔟 Monthly Revenue & Profit Trend with Promotions
# -------------------------------
st.subheader("📈 Monthly Revenue & Profit Trends")
monthly_trend = df_filtered.groupby('month').agg(revenue=('revenue','sum'), profit=('profit','sum')).reset_index()
# Sort months correctly
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=month_order, ordered=True)
monthly_trend = monthly_trend.sort_values('month')

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Scatter(
    x=monthly_trend['month'], 
    y=monthly_trend['revenue'],
    name='Revenue', 
    mode='lines+markers',
    line=dict(color=COLOR_PRIMARY, width=3),
    marker=dict(size=8),
    text=monthly_trend['revenue'].apply(lambda x: f"AED {human_format(x)}"),
    hovertemplate='%{text}<extra></extra>'
))
fig_monthly.add_trace(go.Scatter(
    x=monthly_trend['month'], 
    y=monthly_trend['profit'],
    name='Profit', 
    mode='lines+markers',
    line=dict(color=COLOR_ACCENT, width=3),
    marker=dict(size=8),
    text=monthly_trend['profit'].apply(lambda x: f"AED {human_format(x)}"),
    hovertemplate='%{text}<extra></extra>'
))

# Add promotional period annotations
promo_periods = [
    {'month': 'April', 'name': 'Ramadan Sale', 'color': 'rgba(255, 99, 132, 0.1)'},
    {'month': 'July', 'name': 'Summer Sale', 'color': 'rgba(54, 162, 235, 0.1)'},
    {'month': 'November', 'name': 'Black Friday', 'color': 'rgba(255, 206, 86, 0.1)'}
]

for promo in promo_periods:
    if promo['month'] in monthly_trend['month'].values:
        idx = list(monthly_trend['month']).index(promo['month'])
        fig_monthly.add_vrect(
            x0=idx-0.3, x1=idx+0.3,
            fillcolor=promo['color'],
            layer="below", line_width=0,
            annotation_text=promo['name'],
            annotation_position="top"
        )

fig_monthly.update_layout(
    title='Monthly Revenue & Profit Trend (with Promotional Periods)',
    xaxis_title='Month',
    yaxis_title='Amount (AED)',
    yaxis_tickprefix="AED ",
    yaxis_tickformat=",",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor=COLOR_BG,
    hovermode='x unified',
    height=450
)
st.plotly_chart(fig_monthly, use_container_width=True)

# -------------------------------
# 1️⃣1️⃣ Store Performance Analysis
# -------------------------------
st.subheader("🏬 Store Performance Analysis")

# Load store master to get city information
try:
    stores_df = pd.read_csv(config.FILE_STORES)
    
    # Merge with performance data
    store_perf = df_filtered.groupby(['store_id', 'store_name']).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()
    
    # Convert store_id to same type for successful merge
    # Dashboard data has store_id as category/float, stores file has it as int
    store_perf['store_id'] = store_perf['store_id'].astype(str).str.replace('.0', '', regex=False)
    stores_df['store_id'] = stores_df['store_id'].astype(str)
    
    # Merge with store master data
    store_perf = store_perf.merge(stores_df[['store_id', 'city', 'store_type']], on='store_id', how='left')
    
    # Validate merge was successful
    if store_perf['city'].isna().all() or store_perf['store_type'].isna().all():
        raise ValueError("Merge failed: No matching store_id values found")
    
    col_st1, col_st2 = st.columns(2)
    
    with col_st1:
        # City performance
        city_perf = store_perf.groupby('city').agg(
            revenue=('revenue', 'sum'),
            stores=('store_id', 'count')
        ).reset_index()
        city_perf['avg_per_store'] = city_perf['revenue'] / city_perf['stores']
        city_perf = city_perf.sort_values('revenue', ascending=False)
        
        fig_city = px.bar(
            city_perf, x='city', y='revenue',
            title='Revenue by City',
            labels={'revenue': 'Total Revenue (AED)', 'city': 'City'},
            color='revenue',
            color_continuous_scale=[COLOR_SOFT, COLOR_PRIMARY],
            text='revenue'
        )
        fig_city.update_traces(texttemplate="AED %{text:.2s}", textposition='outside')
        fig_city.update_layout(showlegend=False)
        st.plotly_chart(fig_city, use_container_width=True)
    
    with col_st2:
        # Store type performance
        type_perf = store_perf.groupby('store_type').agg(
            revenue=('revenue', 'sum'),
            stores=('store_id', 'count')
        ).reset_index()
        
        fig_type = px.pie(
            type_perf, names='store_type', values='revenue',
            title='Revenue by Store Type',
            color_discrete_sequence=px.colors.sequential.Teal,
            hole=0.4
        )
        fig_type.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Top performing stores table
    st.markdown("#### Top 10 Performing Stores")
    top_stores_display = store_perf.nlargest(10, 'revenue')[['store_name', 'city', 'store_type', 'revenue', 'profit']]
    top_stores_display['revenue'] = top_stores_display['revenue'].apply(lambda x: f"AED {human_format(x)}")
    top_stores_display['profit'] = top_stores_display['profit'].apply(lambda x: f"AED {human_format(x)}")
    top_stores_display.columns = ['Store', 'City', 'Type', 'Revenue', 'Profit']
    st.dataframe(top_stores_display, use_container_width=True, hide_index=True)
    
except FileNotFoundError:
    st.warning("Store master data not found. Showing basic store performance.")
    top_stores = (
        df_filtered.groupby(['store_id', 'store_name'])
        .agg(revenue=('revenue', 'sum'), profit=('profit', 'sum'))
        .sort_values('revenue', ascending=False)
        .head(10)
        .reset_index()
    )
    top_stores['revenue'] = top_stores['revenue'].map("AED {:,.2f}".format)
    top_stores['profit'] = top_stores['profit'].map("AED {:,.2f}".format)
    st.dataframe(top_stores, use_container_width=True)

# -------------------------------
# 1️⃣2️⃣ Customer Loyalty Segments (if customer data available)
# -------------------------------
st.subheader("👥 Customer Insights")

try:
    customers_df = pd.read_csv(config.FILE_CUSTOMERS)
    
    col_cust1, col_cust2 = st.columns(2)
    
    with col_cust1:
        # Loyalty segment distribution
        loyalty_dist = customers_df['loyalty_segment'].value_counts().reset_index()
        loyalty_dist.columns = ['segment', 'count']
        loyalty_dist['percentage'] = (loyalty_dist['count'] / loyalty_dist['count'].sum() * 100).round(1)
        
        # Define colors for tiers - optimized for dark mode visibility
        tier_colors = {
            'Platinum': '#E8E8E8',  # Bright platinum
            'Gold': '#FFD700',      # Gold (unchanged)
            'Silver': '#B8B8B8'     # Brighter silver for dark mode
        }
        loyalty_dist['color'] = loyalty_dist['segment'].map(tier_colors)
        
        fig_loyalty = px.pie(
            loyalty_dist, names='segment', values='count',
            title='Customer Distribution by Loyalty Tier',
            color='segment',
            color_discrete_map=tier_colors,
            hole=0.4
        )
        fig_loyalty.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_loyalty, use_container_width=True)
    
    with col_cust2:
        # Loyalty tier breakdown table
        loyalty_display = loyalty_dist[['segment', 'count', 'percentage']].copy()
        loyalty_display['percentage'] = loyalty_display['percentage'].apply(lambda x: f"{x}%")
        loyalty_display.columns = ['Loyalty Tier', 'Customers', 'Share']
        st.markdown("#### Loyalty Tier Breakdown")
        st.dataframe(loyalty_display, use_container_width=True, hide_index=True)
        
        # Add insights
        st.markdown("""
        **Tier Characteristics:**
        - 🥇 **Platinum**: Top 10%, ~35% of revenue
        - 🥈 **Gold**: Middle 30%, growth potential
        - 🥉 **Silver**: Base 60%, engagement focus
        """)
        
except FileNotFoundError:
    st.info("💡 Customer loyalty data not available. This would show Platinum/Gold/Silver tier distribution.")

# -------------------------------
# 1️⃣3️⃣ Footer / Export
# -------------------------------
st.markdown("---")
with st.expander("📥 Export Filtered Dataset"):
    st.download_button("Download CSV", data=df_filtered.to_csv(index=False).encode('utf-8'),
                       file_name="bluemart_filtered_data.csv", mime="text/csv")

st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px;'>
    <strong>BlueMart Retail Analytics Dashboard</strong> • 2025 • Built with ❤️ by Amir<br>
    <em>Data-driven insights for omnichannel retail excellence</em>
</div>
""", unsafe_allow_html=True)
