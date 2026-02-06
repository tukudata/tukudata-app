import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Analytics Dashboard Pro",
    page_icon="📊",
    layout="wide"
)

# ========== GENERATE DATA ==========
@st.cache_data
def generate_data():
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    
    data = pd.DataFrame({
        'date': dates,
        'revenue': np.random.normal(1000, 200, 90).cumsum() + 5000,
        'users': np.random.normal(50, 10, 90).cumsum() + 1000,
        'conversion_rate': np.random.uniform(2, 8, 90),
        'bounce_rate': np.random.uniform(30, 60, 90),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 90),
        'product': np.random.choice(['A', 'B', 'C', 'D'], 90),
        'sales': np.random.randint(100, 1000, 90)
    })
    
    products = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Sales': [125000, 98000, 76000, 54000, 32000],
        'Growth': [15.2, -3.4, 22.1, 8.7, 45.3],
        'Market Share': [28.5, 22.1, 17.3, 12.4, 7.8]
    })
    
    return data, products

df, products_df = generate_data()

# ========== HEADER ==========
st.title("📊 Analytics Dashboard Pro")
st.markdown("Real-time insights & performance metrics")

date_col, metric_col = st.columns([3, 1])
with date_col:
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )
with metric_col:
    st.metric("Live Users", "1,245", "12%")

st.markdown("---")

# ========== KPI CARDS ==========
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", "$1.24M", "↑ 15.2%", delta_color="normal")
col2.metric("Active Users", "24.8K", "↑ 8.3%", delta_color="normal")
col3.metric("Avg. Session", "4m 32s", "↓ 2.1%", delta_color="inverse")
col4.metric("Conversion Rate", "4.8%", "↑ 0.8%", delta_color="normal")

# ========== CHARTS ==========
st.markdown("---")
st.subheader("📊 Visualizations")

# Row 1: Line chart and Bar chart
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("**Revenue Trend**")
    st.line_chart(df.set_index('date')['revenue'], height=300)

with chart2:
    st.markdown("**Product Performance**")
    st.bar_chart(products_df.set_index('Product')['Sales'], height=300)

# Row 2: Area chart and Data table
chart3, chart4 = st.columns(2)

with chart3:
    st.markdown("**User Growth**")
    st.area_chart(df.set_index('date')['users'], height=300)

with chart4:
    st.markdown("**Regional Sales**")
    region_sales = df.groupby('region')['sales'].sum()
    st.dataframe(region_sales, height=300)

# Row 3: Matplotlib chart
st.markdown("---")
st.subheader("📈 Matplotlib Chart")

fig, ax = plt.subplots(figsize=(10, 4))
products = products_df['Product']
sales = products_df['Sales']
colors = plt.cm.Set3(np.arange(len(products)) / len(products))
ax.bar(products, sales, color=colors)
ax.set_ylabel('Sales ($)')
ax.set_title('Product Sales Distribution')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# ========== DATA TABLE ==========
st.markdown("---")
st.subheader("📋 Detailed Data")

if st.checkbox("Show raw data"):
    st.dataframe(df, use_container_width=True, height=300)

# ========== DOWNLOAD ==========
st.markdown("---")
csv = df.to_csv(index=False).encode('utf-8')

col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="dashboard_data.csv",
        mime="text/csv"
    )
with col2:
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

# ========== FOOTER ==========
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | v1.0")