import streamlit as st

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("📋 Navigation")
    menu = st.selectbox(
        "Go to",
        ["Home", "Data Input", "Visualization", "About"]
    )
    
    st.divider()
    st.markdown("### Settings")
    dark_mode = st.toggle("Dark Mode", False)
    
    st.divider()
    st.caption("Made with Streamlit")

# ========== MAIN CONTENT ==========
if menu == "Home":
    st.title("Welcome to My App 🎈")
    st.write("This is a clean Streamlit template.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Features")
        st.markdown("""
        - 📊 Data visualization
        - 📁 File upload
        - ⚙️ Custom settings
        - 📈 Real-time updates
        """)
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Show alert", type="primary"):
            st.success("Hello! This is an alert.")
        
        if st.button("Clear cache"):
            st.cache_data.clear()
            st.info("Cache cleared!")

elif menu == "Data Input":
    st.title("📥 Data Input")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv", "txt"]
    )
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        
        # Show preview
        if st.checkbox("Show file preview"):
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)
    
    # Manual input
    with st.form("manual_input"):
        st.subheader("Manual Entry")
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120, 25)
        category = st.selectbox("Category", ["A", "B", "C"])
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"**Submitted:** {name}, {age}, {category}")

elif menu == "Visualization":
    st.title("📊 Visualization")
    
    # Sample chart
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    data = pd.DataFrame({
        'x': np.arange(1, 31),
        'y': np.random.randn(30).cumsum()
    })
    
    st.line_chart(data, x='x', y='y')
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70°F", "1.2°F")
    col2.metric("Pressure", "30.2 psi", "-0.5 psi")
    col3.metric("Humidity", "65%", "3%")

elif menu == "About":
    st.title("ℹ️ About")
    st.write("This is a template Streamlit app.")
    
    with st.expander("Tech Stack"):
        st.code("""
        - Python 3.9+
        - Streamlit
        - Pandas
        - Matplotlib
        """)
    
    st.divider()
    st.caption("Version 1.0 | Last updated: 2024")

# ========== FOOTER ==========
st.divider()
st.caption("Footer area - Add links or contact info here")