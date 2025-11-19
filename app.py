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

# Bluemart color palette
COLOR_PRIMARY = "#005f73"
COLOR_ACCENT = "#0a9396"
COLOR_SOFT = "#94d2bd"
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
# 2️⃣ Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(config.FILE_DASHBOARD_DATA)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
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
# 7️⃣ Revenue by Category
# -------------------------------
rev_category = df_filtered.groupby('category').agg(revenue=('revenue','sum')).reset_index()
fig_category = px.bar(
    rev_category, x='category', y='revenue',
    text='revenue', labels={'revenue':'Revenue (AED)', 'category':'Category'},
    title="Revenue by Category", color='revenue', color_continuous_scale=[COLOR_SOFT, COLOR_PRIMARY]
)
fig_category.update_traces(texttemplate="AED %{text:.2s}", textposition='outside')
st.plotly_chart(fig_category, use_container_width=True)

# -------------------------------
# 8️⃣ Revenue by Channel
# -------------------------------
rev_channel = df_filtered.groupby('channel').agg(revenue=('revenue','sum')).reset_index()
fig_channel = px.pie(rev_channel, names='channel', values='revenue', title="Revenue by Channel",
                     color_discrete_sequence=[COLOR_PRIMARY, COLOR_ACCENT, COLOR_SOFT])
st.plotly_chart(fig_channel, use_container_width=True)

# -------------------------------
# 9️⃣ Monthly Revenue & Profit Trend
# -------------------------------
monthly_trend = df_filtered.groupby('month').agg(revenue=('revenue','sum'), profit=('profit','sum')).reset_index()
# Sort months correctly
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=month_order, ordered=True)
monthly_trend = monthly_trend.sort_values('month')

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Bar(x=monthly_trend['month'], y=monthly_trend['revenue'],
                             name='Revenue', marker_color=COLOR_PRIMARY, text=monthly_trend['revenue'].apply(lambda x: f"AED {human_format(x)}")))
fig_monthly.add_trace(go.Bar(x=monthly_trend['month'], y=monthly_trend['profit'],
                             name='Profit', marker_color=COLOR_ACCENT, text=monthly_trend['profit'].apply(lambda x: f"AED {human_format(x)}")))
fig_monthly.update_layout(
    barmode='group',
    title='Monthly Revenue & Profit Trend',
    xaxis_title='Month',
    yaxis_title='Amount (AED)',
    yaxis_tickprefix="AED ",
    yaxis_tickformat=",",
    legend_title_text='Metric',
    plot_bgcolor=COLOR_BG
)
st.plotly_chart(fig_monthly, use_container_width=True)

# -------------------------------
# 10️⃣ Footer / Export
# -------------------------------
st.markdown("---")
with st.expander("Export filtered dataset"):
    st.download_button("Download CSV", data=df_filtered.to_csv(index=False).encode('utf-8'),
                       file_name="bluemart_filtered_sample.csv", mime="text/csv")

st.markdown("Built for portfolio: BlueMart — 2025 • Author: Amir")
