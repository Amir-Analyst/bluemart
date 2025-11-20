## 🛠️ Technical Implementation

### Technology Stack

- **Data Generation**: Python, Pandas, NumPy
- **Data Processing**: Chunked processing for memory optimization
- **Visualization**: Streamlit, Plotly
- **Analytics**: Statistical analysis, trend identification

### Project Structure

```
bluemart/
├── config.py                 # Central configuration
├── requirements.txt          # Dependencies
├── app.py                    # Streamlit Dashboard
├── scripts/
│   ├── generate_data.py      # Synthetic data generation (5000 SKUs)
│   ├── process_data.py       # Data processing pipeline
│   └── extract_insights.py   # Insight extraction utility
├── data/
│   ├── raw/                  # Generated raw CSVs (11.2M records)
│   └── processed/            # Optimized data for dashboard
└── assets/                   # Visualizations and logo
```

### Key Features

- Realistic data generation with 5,000 SKUs and 11.2M transactions
- Memory-optimized processing using chunking
- Interactive dashboard with real-time filtering
- Scalable architecture for easy extension

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- 8GB+ RAM (for data processing)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bluemart.git
cd bluemart

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# 1. Generate synthetic data
python scripts/generate_data.py

# 2. Process data for dashboard
python scripts/process_data.py

# 3. Launch dashboard
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

---

## 📁 Deliverables

- Cleaned & annotated dataset (all tables, 11.2M records)
- KPI tables & trend analysis
- Interactive Streamlit dashboard
- Insight report with actionable recommendations
- Technical documentation for reproducibility

---

## 🎓 Use Cases

This project demonstrates:

- **Data Engineering**: Large-scale data generation and processing (11.2M records, 5,000 SKUs)
- **Analytics**: KPI calculation, trend analysis, and insight extraction
- **Visualization**: Executive dashboards and data storytelling
- **Business Acumen**: Retail domain knowledge and strategic recommendations
- **Technical Skills**: Python, Pandas, Streamlit, memory optimization

Perfect for showcasing end-to-end analytics capabilities in portfolio presentations.
