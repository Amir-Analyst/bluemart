# BlueMart README - Visualization Guide

This document outlines all the visualizations referenced in the README.md file that need to be created.

## Required Visualizations

### 1. **logo.png**
- **Location**: `assets/logo.png`
- **Description**: BlueMart company logo
- **Status**: ✅ You have this file

### 2. **kpi_overview.png**
- **Location**: `assets/kpi_overview.png`
- **Type**: KPI Dashboard Card Layout
- **Content**: 
  - Total Revenue: AED 1.03 Billion
  - Gross Margin: 31.0%
  - Total Units Sold: 22.9M units
  - Avg Transaction Value: AED 90.00
  - Avg Profit per Order: AED 27.93
- **Style**: Clean dashboard cards with icons, trend indicators (↑/↓), and color coding (green for positive metrics)

### 3. **channel_distribution.png**
- **Location**: `assets/channel_distribution.png`
- **Type**: Pie Chart or Donut Chart
- **Data**:
  - Store: 43.5%
  - Website: 26.6%
  - Mobile App: 17.4%
  - Amazon.ae: 8.7%
  - Noon: 3.9%
- **Style**: Modern, with distinct colors for each channel, percentage labels

### 4. **category_performance.png**
- **Location**: `assets/category_performance.png`
- **Type**: Horizontal Bar Chart
- **Data** (ranked by performance):
  1. Electronics
  2. Snacks
  3. Household
  4. Grocery
  5. Dairy
  6. Personal Care
  7. Beverages
- **Style**: Bars with gradient colors, values labeled, sorted descending

### 5. **monthly_trends.png**
- **Location**: `assets/monthly_trends.png`
- **Type**: Line Chart with Annotations
- **Content**:
  - X-axis: Months (Jan-Dec 2025)
  - Y-axis: Revenue
  - Annotations for promotional periods:
    - Ramadan Sale (April) - spike
    - Summer Sale (July) - moderate increase
    - Black Friday (November) - spike
- **Style**: Smooth line with shaded promotional periods, trend line

### 6. **loyalty_segments.png**
- **Location**: `assets/loyalty_segments.png`
- **Type**: Stacked Bar or Pie Chart
- **Data**:
  - Platinum: 10%
  - Gold: 30%
  - Silver: 60%
- **Style**: Tiered visualization with metallic colors (platinum/silver/gold tones)

### 7. **store_performance_map.png**
- **Location**: `assets/store_performance_map.png`
- **Type**: Geographic Map or Bar Chart by City
- **Data**:
  - Dubai: 25 stores, 50% revenue
  - Abu Dhabi: 15 stores, 30% revenue
  - Sharjah: 10 stores, 20% revenue
- **Style**: UAE map with bubble sizes or simple bar chart with city icons

### 8. **margin_by_category.png**
- **Location**: `assets/margin_by_category.png`
- **Type**: Horizontal Bar Chart with Color Coding
- **Data** (Gross Margin %):
  - Electronics: 40% (🟢 Green)
  - Personal Care: 37% (🟢 Green)
  - Household: 30% (🟡 Yellow)
  - Snacks: 27% (🟡 Yellow)
  - Grocery: 22% (🟡 Yellow)
  - Beverages: 20% (🟠 Orange)
  - Dairy: 17% (🟠 Orange)
- **Style**: Color-coded bars (green/yellow/orange) based on margin health

### 9. **dashboard_overview.png**
- **Location**: `assets/dashboard_overview.png`
- **Type**: Screenshot or Mockup
- **Content**: Screenshot of the Streamlit dashboard showing:
  - KPI cards at top
  - Interactive filters (date, channel, category)
  - Charts and graphs
  - Data table
- **Style**: Professional dashboard screenshot with clean UI

## Visualization Style Guidelines

### Color Palette
- **Primary**: Blue tones (matching BlueMart brand)
- **Accent**: Orange/Gold for highlights
- **Success**: Green (#28a745)
- **Warning**: Yellow/Orange (#ffc107)
- **Danger**: Red (#dc3545)
- **Neutral**: Grays for backgrounds

### Typography
- **Headers**: Bold, clear sans-serif
- **Data Labels**: Readable, not cluttered
- **Legends**: Positioned for easy reading

### General Principles
- **Clean and Modern**: Minimal clutter, focus on data
- **Professional**: Suitable for executive presentations
- **Consistent**: Use same color scheme across all visuals
- **Accessible**: High contrast, readable fonts

## Tools for Creation

Recommended tools:
- **Python**: Matplotlib, Seaborn, Plotly for data visualizations
- **Design Tools**: Canva, Figma for polished graphics
- **Dashboard**: Screenshot from actual Streamlit app
- **Logo**: Your existing BlueMart logo file

## Priority Order

1. **logo.png** - You already have this ✅
2. **kpi_overview.png** - Most important, sets the tone
3. **channel_distribution.png** - Key insight
4. **category_performance.png** - Core business metric
5. **monthly_trends.png** - Shows seasonality
6. **dashboard_overview.png** - Screenshot from app
7. **margin_by_category.png** - Profitability insight
8. **loyalty_segments.png** - Customer insight
9. **store_performance_map.png** - Geographic view

## Notes

- All images should be **high resolution** (at least 1200px wide)
- Use **PNG format** for transparency and quality
- Keep file sizes reasonable (<500KB each) for GitHub
- Ensure all charts are **readable** when displayed in README
