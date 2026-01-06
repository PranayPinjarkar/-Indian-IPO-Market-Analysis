
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(
    page_title="Indian IPO Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #31333F;
        border: 1px solid #e0e0e0;
    }
    .stMetric label {
        color: #31333F !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #31333F !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 Indian IPO Market Analysis")
st.markdown("Analyze historical IPO performance, listing gains, and subscription trends in the Indian Market.")

# Helper to load data
@st.cache_data
def load_data():
    # Attempt to load CSV from current directory
    file_path = "Indian_IPO_Market_Data.csv"
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}. Please ensure the CSV is in the same directory.")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(file_path)
        
        # Strip column names
        df.columns = df.columns.str.strip()
        
        # Convert Date
        # The date format in the file seems to be dd/mm/yy based on previous view (e.g., 03/02/10)
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce')
        df['Year'] = df['Date'].dt.year
        
        # Create Binary Target and Status label
        df['Listing_Gains_Profit'] = df['Listing_Gains_Percent'] > 0
        df['Status'] = df['Listing_Gains_Profit'].apply(lambda x: 'Profit' if x else 'Loss')
        
        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return pd.DataFrame()

df = load_data()

# Only proceed if data is loaded
if not df.empty:
    
    # --- Sidebar Controls ---
    st.sidebar.title("Configuration")
    
    # Year Filter
    all_years = sorted(df['Year'].dropna().astype(int).unique())
    selected_years = st.sidebar.multiselect("Select Year(s)", all_years, default=all_years)
    
    # Apply Filter
    if selected_years:
        filtered_df = df[df['Year'].isin(selected_years)]
    else:
        filtered_df = df
        
    st.sidebar.markdown("---")
    st.sidebar.info(f"Showing {len(filtered_df)} IPOs")

    # --- Main Dashboard ---
    
    # 1. KPI Metrics
    st.subheader("📊 Market Snapshot")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_ipos = len(filtered_df)
    avg_gain = filtered_df['Listing_Gains_Percent'].mean()
    profitable_count = filtered_df['Listing_Gains_Profit'].sum()
    win_rate = (profitable_count / total_ipos * 100) if total_ipos > 0 else 0
    
    kpi1.metric("Total IPOs", f"{total_ipos}")
    kpi2.metric("Avg Listing Gain", f"{avg_gain:.2f}%", delta_color="normal")
    kpi3.metric("Profitable IPOs", f"{profitable_count}")
    kpi4.metric("Success Rate", f"{win_rate:.1f}%")
    
    st.markdown("---")

    # 2. Interactive Charts
    
    # Dynamic Component Selector
    st.subheader("🛠️ Custom Visualization")
    
    chart_type = st.selectbox(
        "Choose Chart Layout",
        ["Distribution Analysis", "Variable Relationships (Scatter)", "Subscription Heatmap", "Company Specific Analysis"]
    )
    
    if chart_type == "Company Specific Analysis":
        st.subheader("🏢 Company Explorer")
        
        # Company Selector
        selected_company = st.selectbox("Select Company", filtered_df['IPOName'].unique())
        
        if selected_company:
            company_data = filtered_df[filtered_df['IPOName'] == selected_company].iloc[0]
            
            # 1. Company Scorecard
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Issue Price", f"₹{company_data['Issue_Price']}")
            col2.metric("Issue Size", f"₹{company_data['Issue_Size']} Cr")
            col3.metric("Listing Gains", f"{company_data['Listing_Gains_Percent']:.2f}%", 
                        delta="Profit" if company_data['Listing_Gains_Profit'] else "Loss")
            col4.metric("Total Subscription", f"{company_data['Subscription_Total']}x")
            
            st.markdown("### Subscription Breakdown")
            
            # 2. Subscription Breakdown (Pie Chart)
            sub_data = {
                'Category': ['QIB', 'HNI', 'RII'],
                'Subscription': [company_data['Subscription_QIB'], company_data['Subscription_HNI'], company_data['Subscription_RII']]
            }
            fig_pie = px.pie(
                sub_data, 
                values='Subscription', 
                names='Category', 
                title=f"Subscription Breakdown for {selected_company}",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.plotly_chart(fig_pie, use_container_width=True)
                
            # 3. Market Comparison
            with col_chart2:
                avg_listing_gain = df['Listing_Gains_Percent'].mean()
                comparison_data = pd.DataFrame({
                    'Entity': [selected_company, 'Market Average'],
                    'Listing Gain (%)': [company_data['Listing_Gains_Percent'], avg_listing_gain]
                })
                
                fig_bar = px.bar(
                    comparison_data, 
                    x='Entity', 
                    y='Listing Gain (%)',
                    color='Entity',
                    title="Performance vs Market Average",
                    color_discrete_map={selected_company: '#00CC96', 'Market Average': '#636EFA'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)

    elif chart_type == "Distribution Analysis":
        col1, col2 = st.columns([1, 3])
        with col1:
            dist_var = st.selectbox("Variable", ["Listing_Gains_Percent", "Issue_Size", "Subscription_Total"])
            bins = st.slider("Number of Bins", 5, 100, 30)
            
        with col2:
            fig_hist = px.histogram(
                filtered_df,
                x=dist_var,
                nbins=bins,
                color="Status" if dist_var == "Listing_Gains_Percent" else None,
                title=f"Distribution of {dist_var}",
                color_discrete_map={"Profit": "#00CC96", "Loss": "#EF553B"},
                marginal="box",
                hover_data=["IPOName", "Date"]
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
    elif chart_type == "Variable Relationships (Scatter)":
        col1, col2, col3 = st.columns(3)
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        
        with col1:
            x_axis = st.selectbox("X-Axis", numeric_cols, index=numeric_cols.index("Issue_Size") if "Issue_Size" in numeric_cols else 0)
        with col2:
            y_axis = st.selectbox("Y-Axis", numeric_cols, index=numeric_cols.index("Listing_Gains_Percent") if "Listing_Gains_Percent" in numeric_cols else 0)
        with col3:
            color_dim = st.selectbox("Color By", ["Status"] + numeric_cols, index=0)
            
        fig_scatter = px.scatter(
            filtered_df,
            x=x_axis,
            y=y_axis,
            color=color_dim,
            size="Issue_Size" if "Issue_Size" in numeric_cols else None,
            hover_name="IPOName",
            hover_data=["Date"],
            title=f"{y_axis} vs {x_axis}",
            color_discrete_map={"Profit": "#00CC96", "Loss": "#EF553B"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    elif chart_type == "Subscription Heatmap":
        st.write("Correlation between different subscription categories and listing gains.")
        
        # Select relevant columns for subscription
        sub_cols = ['Subscription_QIB', 'Subscription_HNI', 'Subscription_RII', 'Subscription_Total', 'Issue_Size', 'Listing_Gains_Percent']
        # Filter for existing columns
        sub_cols = [c for c in sub_cols if c in filtered_df.columns]
        
        if sub_cols:
            corr_mat = filtered_df[sub_cols].corr()
            fig_heat = px.imshow(
                corr_mat,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Correlation Matrix: Subscription & Gains"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("Not enough subscription columns found.")

    st.markdown("---")
    
    # 3. Data Table
    st.subheader("📄 Raw Data Explorer")
    with st.expander("View Full Dataset"):
        st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True)

