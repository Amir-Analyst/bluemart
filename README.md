<div align="center">

![BlueMart Logo](assets/logo.png)

# BlueMart Retail LLC — 2025 Analytics Project

**Transforming Retail Through Data-Driven Insights**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-green.svg)](https://pandas.pydata.org/)

</div>

---

## 📊 Company Overview

**BlueMart Retail LLC** is a UAE-based omnichannel retailer operating **50 stores** across Dubai, Abu Dhabi, and Sharjah, with a strong e-commerce presence through its website, mobile app, and marketplace partnerships (Amazon.ae, Noon).

- **Product Range**: 5,000 SKUs across 7 categories (Electronics, Personal Care, Household, Grocery, Dairy, Beverages, Snacks)
- **Customer Base**: ~5,000 registered customers segmented into loyalty tiers (Silver, Gold, Platinum)
- **Objective**: Integrate physical and digital channels, optimize inventory, and leverage analytics for data-driven decisions

---

## 🎯 Business Challenge

BlueMart faces typical mid-sized retailer challenges:

- **Inventory Management**: Optimal stock levels across 50 stores with 5,000 SKUs
- **Demand Forecasting**: Prevent stockouts and overstock situations
- **Customer Behavior**: Understand purchasing patterns and channel preferences
- **Channel Performance**: Optimize across store, website, mobile, and marketplaces
- **Promotion ROI**: Assess seasonal and promotional effectiveness

---

## 💡 Project Goal

Build a KPI-driven analytics framework to provide visibility into sales, inventory, promotions, and customer behavior, enabling data-driven decisions to improve revenue, margins, and operational efficiency.

---

## 📈 Dataset Overview

| Aspect | Details |
|--------|---------|
| **Time Period** | Jan 1 – Dec 31, 2025 (daily granularity) |
| **Stores** | 50 stores (Mall, High Street, Community) |
| **SKU Universe** | 5,000 SKUs across 7 categories |
| **Customers** | ~5,000 registered customers |
| **Channels** | Store, Website, Mobile App, Amazon.ae, Noon |
| **Transaction Volume** | 11.2M sales records |

### Data Tables

| Table | Rows | Description |
|-------|------|-------------|
| **Store Master** | 50 | store_id, store_name, city, store_type, opening_date |
| **SKU Master** | 5,000 | sku_id, sku_name, category, subcategory, unit_price, cost_price, brand |
| **Customer Master** | 5,000 | cust_id, age, gender, city, loyalty_segment, registration_date |
| **Sales Transactions** | 11.2M | date, store_id, sku_id, customer_id, quantity, unit_price, total_value, channel, discount_pct |
| **Inventory Snapshot** | 75,000 | store_id, sku_id, stock_on_hand, reorder_point, snapshot_date |
| **Promotions** | 9 | promo_id, promo_name, start_date, end_date, discount_pct, promo_type |

---

## 🔑 Key Performance Indicators

### Executive Summary Metrics

| KPI | 2025 Performance | Insight |
|-----|------------------|---------|
| **Total Revenue** | AED 896.4M | Strong omnichannel performance |
| **Gross Margin** | 30.0% | Consistent profitability across categories |
| **Total Units Sold** | 22.4M units | High transaction volume |
| **Avg Transaction Value** | AED 80.12 | Consistent basket size |
| **Avg Profit per Order** | AED 24.05 | Effective pricing strategy |

> **Note**: Visualizations in this README are illustrative. For exact metrics, refer to the interactive dashboard or summary_metrics.json.

---

## 📊 Channel Performance

### Revenue Distribution

| Channel | Revenue Share | Revenue (AED) |
|---------|---------------|---------------|
| **Store** | 50.0% | 448.5M |
| **Website** | 25.0% | 224.2M |
| **Mobile App** | 15.0% | 134.1M |
| **Amazon.ae** | 7.0% | 62.6M |
| **Noon** | 3.0% | 26.9M |

### Key Insights
- Physical stores remain the core revenue driver at 50%
- Digital channels (Website + Mobile) account for 40% of revenue
- Marketplace channels (Amazon.ae + Noon) contribute 10%, providing incremental reach

---

## 🛍️ Category Performance

### Revenue by Category

| Category | Revenue Share | Revenue (AED) | Margin % |
|----------|---------------|---------------|----------|
| **Electronics** | 46.5% | 416.8M | 29.8% |
| **Personal Care** | 14.2% | 127.4M | 30.1% |
| **Household** | 11.4% | 101.8M | 30.0% |
| **Grocery** | 9.7% | 86.9M | 30.2% |
| **Dairy** | 8.2% | 73.1M | 30.3% |
| **Beverages** | 5.5% | 49.1M | 30.4% |
| **Snacks** | 4.6% | 41.4M | 30.4% |

### Category Insights
- **Electronics dominates** with 46.5% revenue share and consistent 30% margin
- All categories maintain healthy 30% gross margins
- **FMCG categories** (Grocery, Dairy, Beverages, Snacks) drive traffic and frequent purchases

---

## 🏪 Store Performance

### Geographic Distribution

| City | Revenue Share | Revenue (AED) |
|------|---------------|---------------|
| **Dubai** | 56.0% | 501.8M |
| **Abu Dhabi** | 28.0% | 251.1M |
| **Sharjah** | 16.0% | 143.5M |

### Store Type Analysis

| Store Type | Count | Characteristics |
|------------|-------|-----------------|
| **Mall** | 20 | High footfall, premium categories, weekend peaks |
| **High Street** | 20 | Consistent traffic, convenience-focused |
| **Community** | 10 | Essential goods, frequent purchases |

---

## 📅 Seasonal Trends

### Top Revenue Months

| Month | Revenue (AED) |
|-------|---------------|
| **July** | 105.3M |
| **December** | 92.8M |
| **October** | 92.6M |

### Promotional Impact

| Promotion | Period | Type | Key Categories |
|-----------|--------|------|----------------|
| **Ramadan Sale** | April | Religious | Grocery, Beverages, Dairy |
| **Summer Sale** | July | Seasonal | Personal Care, Beverages |
| **Black Friday** | November | Retail Event | Electronics, Household |

**Key Finding**: July (Summer Sale) generated the highest monthly revenue, followed by year-end shopping in December.

---

## 🎯 Customer Insights

### Loyalty Segmentation

| Tier | Customer % | Strategic Focus |
|------|------------|-----------------|
| **Platinum** | 10% | VIP experiences, exclusive previews |
| **Gold** | 30% | Targeted promotions, upgrade incentives |
| **Silver** | 60% | Engagement campaigns, loyalty building |

**Insight**: Platinum customers (10% of base) generate approximately 35% of revenue, making them critical for retention strategies.

---

## 🚀 Key Insights & Findings

### 1. Electronics-Driven Revenue
Electronics accounts for nearly half of all revenue (46.5%) while maintaining healthy 30% margins. This category is the primary profit driver.

### 2. Omnichannel Balance
Physical stores contribute 50% of revenue, with digital channels (40%) showing strong growth. This validates the omnichannel investment strategy.

### 3. Geographic Concentration
Dubai generates 56% of revenue, indicating strong market presence in the emirate. Opportunities exist for expansion in Abu Dhabi and Sharjah.

### 4. Seasonal Peaks
July (Summer Sale) and December (year-end shopping) are peak revenue months, requiring strategic inventory planning.

### 5. Consistent Margins
All categories maintain 30% gross margins, indicating effective pricing and cost management across the product portfolio.

---

## 📋 Strategic Recommendations

### Sales & Marketing

**1. Mobile App Growth**
- Current: 15% revenue share (AED 134M)
- Target: 20% through app-exclusive flash sales on high-margin Electronics
- Expected Impact: +AED 45M annual revenue

**2. Marketplace Expansion**
- Expand Amazon.ae SKU range from 5,000 to 7,500, focusing on high-margin Personal Care and Snacks
- Reposition Noon as clearance channel for Electronics
- Expected Impact: +AED 25M annual revenue

**3. Customer Tier Activation**
- Launch "Gold Member Double Points" on Grocery + Dairy (off-peak days)
- Create Silver-to-Gold upgrade path through Electronics purchases
- Expected Impact: +15% Gold tier transaction frequency

### Inventory & Supply Chain

**1. SKU Optimization**
- Focus on top 20% of SKUs generating 80% of revenue
- Implement daily demand forecasting for fast-moving Electronics
- Clear bottom 10% of slow-moving SKUs quarterly

**2. Store-Type Allocation**
- **Mall Stores**: 60% Electronics, 15% Personal Care, 25% other
- **Community Stores**: 50% Grocery+Dairy, 30% Household, 20% Snacks
- **High Street**: Balanced 35% Electronics, 25% Personal Care, 40% FMCG

**3. Seasonal Planning**
- **July (Summer)**: Stock up Personal Care (+50%), Beverages (+40%)
- **December (Year-end)**: Focus on Electronics (+80%), Household (+30%)
- Begin stock build-up 3 weeks before peak periods

### Executive Leadership

**1. Digital Channel Investment**
- Target: Increase digital share from 40% to 50% by Q4 2026
- Invest in AI-powered recommendations (AED 150K) for website
- Implement push notifications for mobile app (AED 80K)

**2. Geographic Expansion**
- Open 3 new stores in Dubai (highest per-store revenue)
- Target locations: Dubai Marina, JBR, Business Bay
- Expected Impact: +AED 45M annual revenue

**3. Private Label Development**
- Launch "BlueMart Essentials" in Household category
- Target: 20 SKUs with 45% margins (vs 30% branded)
- Expected Impact: +AED 30M revenue, margin improvement to 32%

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Amir Khan**  
Data Analyst | Retail Analytics Specialist  
[LinkedIn](https://www.linkedin.com/in/amir-khan-hussain/) | [Portfolio](https://amir-analyst.github.io/) | [Email](mailto:amirmailforbusiness@gmail.com)

---

<div align="center">

**Built with data-driven retail excellence in mind**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

</div>
