import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Analytics Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Metrics cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #f0f0f0;
    }
    
    /* Custom headers */
    .section-header {
        border-left: 5px solid #667eea;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
        color: #2c3e50;
    }
    
    /* DataTables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== GENERATE SAMPLE DATA ==========
@st.cache_data
def generate_data():
    # Time series data
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    
    # Multiple metrics
    np.random.seed(42)
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
    
    # Top products data
    products = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Sales': [125000, 98000, 76000, 54000, 32000],
        'Growth': [15.2, -3.4, 22.1, 8.7, 45.3],
        'Market Share': [28.5, 22.1, 17.3, 12.4, 7.8]
    })
    
    return data, products

# Load data
df, products_df = generate_data()

# ========== HEADER ==========
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.title("📊 Analytics Dashboard Pro")
    st.markdown("Real-time insights & performance metrics")
with col2:
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )
with col3:
    st.metric("Live Users", "1,245", "12%")

st.markdown("---")

# ========== KPI CARDS ==========
st.markdown('<h3 class="section-header">Key Performance Indicators</h3>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Revenue", "$1.24M", "↑ 15.2%", delta_color="normal")
    st.markdown('</div>', unsafe_allow_html=True)

with kpi2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Active Users", "24.8K", "↑ 8.3%", delta_color="normal")
    st.markdown('</div>', unsafe_allow_html=True)

with kpi3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Avg. Session", "4m 32s", "↓ 2.1%", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with kpi4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Conversion Rate", "4.8%", "↑ 0.8%", delta_color="normal")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== CHARTS ROW 1 ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Revenue Trend")
    
    # Interactive time series with Plotly
    fig = px.line(df, x='date', y='revenue', 
                  template='plotly_white',
                  height=400)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌍 Regional Distribution")
    
    # Donut chart
    region_data = df.groupby('region')['sales'].sum().reset_index()
    fig = px.pie(region_data, values='sales', names='region',
                 hole=0.5, color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== CHARTS ROW 2 ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Product Performance")
    
    # Bar chart with growth indicators
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=products_df['Product'],
        y=products_df['Sales'],
        marker_color=px.colors.qualitative.Pastel,
        text=products_df['Sales'].apply(lambda x: f'${x/1000:.1f}K'),
        textposition='outside'
    ))
    fig.update_layout(
        height=400,
        yaxis_title="Sales ($)",
        xaxis_title="Product",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📉 Conversion vs Bounce Rate")
    
    # Scatter plot
    fig = px.scatter(df, x='conversion_rate', y='bounce_rate',
                     color='region', size='sales',
                     hover_data=['date'],
                     template='plotly_white',
                     height=400)
    fig.update_layout(
        xaxis_title="Conversion Rate (%)",
        yaxis_title="Bounce Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== DATA TABLE & CONTROLS ==========
st.markdown('<h3 class="section-header">📋 Detailed Data</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col2:
    show_raw = st.toggle("Show Raw Data", False)
    rows_to_show = st.slider("Rows", 5, 50, 10)

if show_raw:
    st.dataframe(df.sort_values('date', ascending=False).head(rows_to_show),
                 use_container_width=True,
                 height=400)

# ========== DOWNLOAD SECTION ==========
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Export Data")
    
    # Convert to CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="dashboard_data.csv",
        mime="text/csv",
        icon="📄"
    )

with col2:
    st.subheader("🔄 Refresh Data")
    if st.button("🔄 Update Dashboard", type="primary"):
        st.cache_data.clear()
        st.rerun()

# ========== FOOTER ==========
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("📅 Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
with footer_col2:
    st.caption("📊 Data refreshed every 15 minutes")
with footer_col3:
    st.caption("🔒 Secure connection • v2.1.0")