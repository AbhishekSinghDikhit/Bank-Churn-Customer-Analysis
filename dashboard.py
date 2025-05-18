import streamlit as st
from PIL import Image
import os
import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set page configuration with favicon
st.set_page_config(
    layout="wide",
    page_title="📊 Bank Customer Churn Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
        /* Modern Font Import */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
        
        /* Global styles */
        .main {
            background-color: #F8FAFC;
            padding: 1.5rem 2rem;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            color: #1E293B;
            line-height: 1.6;
        }
        
        h1, h2, h3, h4 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: #0F172A;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #1E40AF, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        h2 {
            font-size: 1.75rem;
            margin-top: 1rem;
            color: #1E40AF;
        }
        
        h3 {
            font-size: 1.35rem;
            color: #0F172A;
            margin-top: 1rem;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.5rem;
        }
        
        /* Cards */
        .card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-top: 4px solid #3B82F6;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Metrics */
        .metric-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
            border-left: 4px solid #3B82F6;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1E40AF;
            margin-bottom: 0.3rem;
        }
        
        .metric-label {
            color: #64748B;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #F1F5F9;
        }
        
        .sidebar .sidebar-content {
            background-color: #FFFFFF;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        /* Form fields */
        input[type="text"], input[type="email"] {
            width: 100%;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: border-color 0.3s ease;
        }
        
        input[type="text"]:focus, input[type="email"]:focus {
            border-color: #3B82F6;
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #1E40AF, #3B82F6);
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px;
            transition: all 0.3s ease !important;
            width: 100%;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.15);
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #1E3A8A, #2563EB);
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(59, 130, 246, 0.2);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #F8FAFC;
            border-radius: 10px;
            padding: 0.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            border-radius: 8px;
            color: #64748B;
            font-weight: 500;
            font-size: 0.95rem;
            background-color: transparent;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: white !important;
            color: #1E40AF !important;
            font-weight: 600;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #0F172A;
            background-color: #F1F5F9;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        
        .streamlit-expanderContent {
            border: 1px solid #E2E8F0;
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 1.25rem;
        }
        
        /* Chart Container */
        .chart-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            padding: 1rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
            border-left: 4px solid #3B82F6;
        }
        
        .chart-container img {
            border-radius: 8px;
            margin-top: 0.5rem;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem;
            background-color: #F1F5F9;
            border-radius: 10px;
            margin-top: 2rem;
            color: #64748B;
            font-size: 0.85rem;
        }
        
        .footer a {
            color: #2563EB;
            text-decoration: none;
            font-weight: 500;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Data table */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        /* Info, success, warning boxes */
        .stAlert {
            border-radius: 8px;
            border: none !important;
            padding: 0.75rem 1rem !important;
        }
        
        .stAlert > div {
            padding: 0.5rem 0.75rem !important;
            border-radius: 6px;
        }
        
        /* Dividers */
        hr {
            margin: 1.5rem 0;
            border: none;
            height: 1px;
            background-color: #E2E8F0;
        }
    </style>
""", unsafe_allow_html=True)

# Current date for dashboard
current_date = datetime.now().strftime("%B %d, %Y")

# Sidebar with user input form and branding
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 1.5rem;">
            <h2 style="margin-bottom: 0;">💼 Bank<span style="color: #3B82F6;">Vision</span></h2>
            <p style="color: #64748B; font-size: 0.9rem; margin-top: 0;">Customer Insights Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🔐 User Login")
    with st.form(key='user_form'):
        user_name = st.text_input("Full Name", placeholder="Enter your name", help="Required")
        user_email = st.text_input("Email Address", placeholder="Enter your email", help="Required")
        submitted = st.form_submit_button("Sign In", type="primary")

    # Validate form input
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not submitted:
        st.info("ℹ️ Please fill out the form to access the dashboard.")
        st.stop()
    elif not user_name or not user_email:
        st.warning("⚠️ Both Name and Email are required.")
        st.stop()
    elif not re.match(email_pattern, user_email.strip()):
        st.error("❌ Invalid email format (e.g., example@domain.com).")
        st.stop()
    else:
        st.success("✅ Authentication successful!")
    
    # Additional sidebar sections
    st.markdown("#### 📌 Quick Links")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style="padding: 0.6rem; text-align: center; background-color: #EFF6FF; border-radius: 6px; cursor: pointer;">
                <span style="font-size: 0.85rem; font-weight: 500; color: #1E40AF;">📊 Reports</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="padding: 0.6rem; text-align: center; background-color: #EFF6FF; border-radius: 6px; cursor: pointer;">
                <span style="font-size: 0.85rem; font-weight: 500; color: #1E40AF;">🔔 Alerts</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="margin-top: 1rem; padding: 1rem; background-color: #F0FDF4; border-radius: 8px; border-left: 3px solid #22C55E;">
            <p style="margin: 0; font-size: 0.9rem; color: #166534;">
                <strong>👋 Need help?</strong><br>
                Contact our support team for assistance with your dashboard.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Function to save user info
@st.cache_data
def save_user_info(user_name, user_email, file_path="data/user_info.csv"):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Login Date'])
        writer.writerow([user_name, user_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# Save user info
save_user_info(user_name, user_email)

# Load dataset
data_path = "data/Bank Customer Churn Prediction.csv"
if not os.path.exists(data_path):
    st.error("❌ Dataset file not found in 'data/' directory.")
    st.stop()
df = pd.read_csv(data_path)

# Create plots directory
plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Function to save plots with optimized quality
def save_plot(fig, filename):
    filepath = os.path.join(plot_dir, filename)
    # Save the figure using Matplotlib without optimize or quality
    fig.savefig(filepath, bbox_inches='tight', dpi=300, format='png')
    plt.close(fig)
    
    # Optional: Optimize the PNG using Pillow
    try:
        img = Image.open(filepath)
        img.save(filepath, format='PNG', optimize=True)
    except Exception as e:
        print(f"Warning: Could not optimize PNG {filename}: {e}")
    
    return filepath

# Set consistent chart style with improved aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'legend.frameon': True,
    'legend.framealpha': 0.8,
    'legend.fontsize': 10,
    'figure.figsize': (10, 6),
})

# Color palette for visualizations
colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

# Dashboard header with animation
st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1.5rem 0;" class="fadeIn">
        <h1>📊 Bank Customer Churn Dashboard</h1>
        <p style="color: #64748B; font-size: 1.1rem; margin-top: 0;">
            Uncover insights to drive customer retention strategies
        </p>
        <p style="color: #94A3B8; font-size: 0.85rem;">Last updated: """ + current_date + """</p>
    </div>
""", unsafe_allow_html=True)

# Welcome message and key metrics
st.markdown(f"""
    <div style="background: linear-gradient(to right, #EFF6FF, #DBEAFE); 
         padding: 1.25rem; border-radius: 10px; margin-bottom: 1.5rem;" class="fadeIn">
        <h3 style="color: #0C0950; margin-top: 0; border: none; padding: 0;">👋 Welcome, {user_name}!</h3>
        <p style="margin-bottom: 0.5rem; color: #161179">
            Your bank customer churn analysis dashboard is ready. 
            Explore the insights below to understand customer behavior patterns.
        </p>
    </div>
""", unsafe_allow_html=True)

# Key metrics row
def format_number(num):
    return f"{num:,.0f}" if num >= 1000 else f"{num:.0f}"

# Calculate key metrics
total_customers = len(df)
churned_customers = df['churn'].sum()
churn_rate = (churned_customers / total_customers) * 100
avg_balance = df['balance'].mean()
avg_age = df['age'].mean()

metrics_col1, metrics_col2, metrics_col3, metrics_col4, metrics_col5 = st.columns(5)

with metrics_col1:
    st.markdown("""
        <div class="metric-card">
            <p class="metric-value">""" + format_number(total_customers) + """</p>
            <p class="metric-label">Total Customers</p>
        </div>
    """, unsafe_allow_html=True)

with metrics_col2:
    st.markdown("""
        <div class="metric-card" style="border-left-color: #EF4444;">
            <p class="metric-value" style="color: #EF4444;">""" + format_number(churned_customers) + """</p>
            <p class="metric-label">Churned Customers</p>
        </div>
    """, unsafe_allow_html=True)

with metrics_col3:
    st.markdown("""
        <div class="metric-card" style="border-left-color: #F59E0B;">
            <p class="metric-value" style="color: #F59E0B;">""" + f"{churn_rate:.1f}%" + """</p>
            <p class="metric-label">Churn Rate</p>
        </div>
    """, unsafe_allow_html=True)

with metrics_col4:
    st.markdown("""
        <div class="metric-card" style="border-left-color: #10B981;">
            <p class="metric-value" style="color: #10B981;">$""" + format_number(avg_balance) + """</p>
            <p class="metric-label">Avg. Balance</p>
        </div>
    """, unsafe_allow_html=True)

with metrics_col5:
    st.markdown("""
        <div class="metric-card" style="border-left-color: #8B5CF6;">
            <p class="metric-value" style="color: #8B5CF6;">""" + f"{avg_age:.1f}" + """</p>
            <p class="metric-label">Avg. Age</p>
        </div>
    """, unsafe_allow_html=True)

# About section
with st.expander("📘 About This Dashboard", expanded=False):
    # Apply CSS for styling Streamlit components
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Roboto:wght@400;500&display=swap');

            /* Style Streamlit's markdown elements within the expander */
            .st-expander .stMarkdown h3 {
                font-family: 'Inter', sans-serif;
                font-size: 20px;
                font-weight: 700;
                color: #1E3A8A;
                margin-bottom: 0.5rem;
            }

            .st-expander .stMarkdown p, .st-expander .stMarkdown ul {
                font-family: 'Roboto', sans-serif;
                font-size: 16px;
                color: #1F2937;
                line-height: 1.5;
                margin-bottom: 1rem;
            }

            .st-expander .stMarkdown ul li {
                margin-bottom: 0.5rem;
            }

            .pro-tip-native {
                animation: fadeIn 0.5s ease-out;
                background-color: #E6FFFA;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
                border-left: 4px solid #2DD4BF;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .pro-tip-native p {
                margin: 0;
                color: #1E3A8A;
                font-weight: 500;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)

    # Content using Streamlit-native components
    st.subheader("Bank Customer Churn Analysis")
    st.write("This dashboard provides comprehensive insights into customer churn patterns to help inform targeted retention strategies.")

    st.subheader("Dataset Information")
    st.markdown("""
        - **Source:** Bank Customer Churn Prediction dataset
        - **Size:** 10,000 customer records
        - **Features:** Credit Score, Geography, Gender, Age, Tenure, Balance, Products, Credit Card, Active Member, Salary, Churn
    """)

    st.subheader("How to Use This Dashboard")
    st.write("Use the visualizations to identify high-risk customer segments and patterns in churn behavior. The insights can inform tailored retention strategies for different customer groups.")

    with st.container():
        st.markdown("""
            <div class="pro-tip-native">
                <p><strong>💡 Pro Tip:</strong> Focus on segments with high churn rates but also high customer value to prioritize your retention efforts.</p>
            </div>
        """, unsafe_allow_html=True)


# Generate visualizations
with st.spinner("Generating visualizations..."):
    # 1. Improved Churn Rate Pie Chart
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    explode = (0, 0.1)  # explode the 2nd slice (Churned)
    wedges, texts, autotexts = ax1.pie(
        df['churn'].value_counts(), 
        labels=['Retained', 'Churned'],
        autopct='%1.1f%%',
        explode=explode,
        colors=[colors[0], colors[3]],
        startangle=90,
        shadow=False,
        wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 1},
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': '#333333'}
    )
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.title('Customer Churn Distribution', fontsize=16, pad=20)
    # Change text colors for better visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
    pie_chart_path = save_plot(fig1, "churn_distribution.png")

    # 2. Improved Churn by Country with annotations
    country_churn = df.groupby('country')['churn'].mean() * 100
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(
        x=country_churn.index,
        y=country_churn.values,
        palette=[colors[0], colors[1], colors[2]],
        ax=ax2
    )
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars.patches):
        ax2.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{country_churn.values[i]:.1f}%',
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='#333333'
        )
    
    ax2.set_title('Churn Rate by Country', fontsize=16, pad=20)
    ax2.set_ylabel('Churn Rate (%)', fontsize=12)
    ax2.set_xlabel('Country', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, max(country_churn.values) * 1.2)  # Add space for labels
    country_chart_path = save_plot(fig2, "churn_rate_by_country.png")

    # 3. Improved Churn by Age Group with gradient
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 100], labels=['<30', '30-40', '40-50', '50+'])
    age_churn = df.groupby('age_group')['churn'].mean() * 100
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    # Create a color gradient
    gradient_colors = [colors[1], colors[2], colors[2], colors[3]]
    
    bars = sns.barplot(
        x=age_churn.index,
        y=age_churn.values,
        palette=gradient_colors,
        ax=ax3
    )
    
    # Add value labels
    for i, bar in enumerate(bars.patches):
        ax3.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{age_churn.values[i]:.1f}%',
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='#333333'
        )
    
    ax3.set_title('Churn Rate by Age Group', fontsize=16, pad=20)
    ax3.set_ylabel('Churn Rate (%)', fontsize=12)
    ax3.set_xlabel('Age Group', fontsize=12)
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_ylim(0, max(age_churn.values) * 1.2)  # Add space for labels
    
    # Add insights annotation
    if max(age_churn.values) > 25:
        ax3.annotate(
            'Higher churn risk in 50+ age group',
            xy=(3, age_churn.values[3]),
            xytext=(3.2, age_churn.values[3] + 3),
            arrowprops=dict(arrowstyle='->', color='#475569'),
            fontsize=10,
            color='#475569',
            backgroundcolor='white',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.8)
        )
    
    age_chart_path = save_plot(fig3, "churn_by_age.png")

    # 4. Improved Churn by Active Member Status
    active_churn = df.groupby('active_member')['churn'].mean() * 100
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(
        x=[0, 1],
        y=active_churn.values,
        palette=[colors[3], colors[0]],
        ax=ax4
    )
    
    # Add value labels
    for i, bar in enumerate(bars.patches):
        ax4.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{active_churn.values[i]:.1f}%',
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='#333333'
        )
    
    ax4.set_title('Churn Rate by Active Member Status', fontsize=16, pad=20)
    ax4.set_ylabel('Churn Rate (%)', fontsize=12)
    ax4.set_xticklabels(['Inactive', 'Active'], fontsize=12)
    ax4.set_xlabel('Member Status', fontsize=12)
    ax4.grid(axis='y', alpha=0.3)
    ax4.set_ylim(0, max(active_churn.values) * 1.2)  # Add space for labels
    
    # Add insights annotation
    max_index = np.argmax(active_churn.values)
    if max_index == 0 and active_churn.values[0] > active_churn.values[1] * 1.5:
        ax4.annotate(
            'Inactive members are high-risk',
            xy=(0, active_churn.values[0]),
            xytext=(0, active_churn.values[0] + 3),
            arrowprops=dict(arrowstyle='->', color='#475569'),
            fontsize=10,
            color='#475569',
            backgroundcolor='white',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.8)
        )
    
    active_chart_path = save_plot(fig4, "churn_by_active_member.png")

    # 5. Improved Estimated Salary Distribution with KDE
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    # Create separate distributions for churned and non-churned
    sns.histplot(
        data=df, x='estimated_salary', hue='churn',
        palette=[colors[0], colors[3]],
        element='step', kde=True, 
        alpha=0.6, bins=30,
        ax=ax5
    )
    
    ax5.set_title('Estimated Salary Distribution by Churn Status', fontsize=16, pad=20)
    ax5.set_xlabel('Estimated Salary ($)', fontsize=12)
    ax5.set_ylabel('Count', fontsize=12)
    ax5.grid(True, alpha=0.3)
    ax5.legend(labels=['Retained', 'Churned'], title='Customer Status', title_fontsize=12)
    
    salary_chart_path = save_plot(fig5, "estimated_salary.png")
    
    # 6. New: Credit Score vs Churn - Scatter plot
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    
    # Calculate average churn rate by credit score ranges
    df['credit_score_bin'] = pd.cut(df['credit_score'], bins=10)
    credit_score_churn = df.groupby('credit_score_bin')['churn'].mean() * 100
    
    # Plot points with size based on count in each bin
    bin_counts = df['credit_score_bin'].value_counts().sort_index()
    
    # Get the midpoint of each bin for x-axis
    midpoints = [(interval.left + interval.right)/2 for interval in credit_score_churn.index]
    
    # Plot scatter with size proportional to bin count
    scatter = ax6.scatter(
        midpoints,
        credit_score_churn.values,
        s=bin_counts.values/10,  # Scale down the sizes for better visualization
        alpha=0.7,
        c=credit_score_churn.values,
        cmap='coolwarm',
        edgecolor='black',
        linewidth=0.5
    )
    
    # Add trend line
    z = np.polyfit(midpoints, credit_score_churn.values, 1)
    p = np.poly1d(z)
    ax6.plot(midpoints, p(midpoints), '--', color='#475569', linewidth=2)
    
    ax6.set_title('Churn Rate by Credit Score', fontsize=16, pad=20)
    ax6.set_xlabel('Credit Score', fontsize=12)
    ax6.set_ylabel('Churn Rate (%)', fontsize=12)
    ax6.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax6)
    cbar.set_label('Churn Rate (%)', fontsize=10)
    
    credit_score_chart_path = save_plot(fig6, "churn_by_credit_score.png")

# Dashboard with Tabs
tab1, tab2, tab3 = st.tabs(["📈 Churn Analysis", "🔍 Customer Segments", "📊 Summary Statistics"])

# Tab 1: Churn Analysis
with tab1:
    st.markdown("""
        <h2 class="fadeIn">📈 Churn Analysis Dashboard</h2>
        <p style="color: #64748B;">Explore key insights on customer churn patterns and trends</p>
    """, unsafe_allow_html=True)
    
    # Two-column layout for main charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Overall Churn Distribution
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(pie_chart_path):
            st.image(Image.open(pie_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Approximately 20% of customers have churned, suggesting 
                        room for improvement in customer retention strategies.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Churn by Active Member Status
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(active_chart_path):
            st.image(Image.open(active_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Inactive customers have significantly higher churn rates.
                        Re-engagement campaigns should be prioritized for this segment.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Second row with geographical and age insights
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Churn Rate by Country
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(country_chart_path):
            st.image(Image.open(country_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Churn rates vary by country, with some regions showing
                        significantly higher rates. Consider tailored regional strategies.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Churn Rate by Age Group
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(age_chart_path):
            st.image(Image.open(age_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Older customers (50+) have the highest churn rate,
                        suggesting a need for age-specific retention strategies.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Full width for remaining charts
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Salary Distribution by Churn Status
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(salary_chart_path):
            st.image(Image.open(salary_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Salary distribution is similar for both churned and retained
                        customers, suggesting income alone is not a strong predictor of churn.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
            <div class="chart-container fadeIn">
                <h3 style="font-size: 1.2rem; border: none; margin-top: 0; padding-bottom: 0.5rem; color: #2D336B;">
                    Churn Rate by Credit Score
                </h3>
        """, unsafe_allow_html=True)
        
        if os.path.exists(credit_score_chart_path):
            st.image(Image.open(credit_score_chart_path), use_container_width=True)
        else:
            st.warning("⚠️ Chart image not found")
            
        st.markdown("""
                <div style="margin-top: 0.5rem;">
                    <p style="font-size: 0.9rem; color: #FFFFFF;">
                        <strong>Key Insight:</strong> Lower credit scores tend to correlate with higher churn rates,
                        indicating a potential risk factor for customer attrition.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Recommendations section
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color: #F0F9FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #0EA5E9;">
            <h3 style="color: #0369A1; margin-top: 0; border: none; padding: 0;">💡 Strategic Recommendations</h3>
            <ul style="margin-bottom: 0; color: #000000;">
                <li><strong>Inactive Members:</strong> Implement a re-engagement campaign offering personalized incentives.</li>
                <li><strong>Older Customers (50+):</strong> Develop age-appropriate services and dedicated support channels.</li>
                <li><strong>Regional Focus:</strong> Create country-specific retention strategies for high-churn regions.</li>
                <li><strong>At-Risk Identification:</strong> Use a combination of activity status, age, and credit score to flag customers at risk.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Tab 2: Customer Segments
with tab2:
    st.markdown("""
        <h2 class="fadeIn">🔍 Customer Segment Analysis</h2>
        <p style="color: #64748B;">Analyze churn patterns across different customer segments</p>
    """, unsafe_allow_html=True)
    
    # Create feature columns for filtering
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        selected_country = st.selectbox(
            "Select Country",
            options=["All"] + sorted(df["country"].unique().tolist())
        )
    
    with filter_col2:
        selected_age_group = st.selectbox(
            "Select Age Group",
            options=["All", "<30", "30-40", "40-50", "50+"]
        )
    
    with filter_col3:
        selected_active = st.selectbox(
            "Active Member Status",
            options=["All", "Active", "Inactive"]
        )
    
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]
    
    if selected_age_group != "All":
        filtered_df = filtered_df[filtered_df["age_group"] == selected_age_group]
    
    if selected_active != "All":
        active_map = {"Active": 1, "Inactive": 0}
        filtered_df = filtered_df[filtered_df["active_member"] == active_map[selected_active]]
    
    # Show filtered segment metrics
    segment_size = len(filtered_df)
    segment_churn = filtered_df["churn"].sum()
    segment_churn_rate = (segment_churn / segment_size * 100) if segment_size > 0 else 0
    segment_avg_balance = filtered_df["balance"].mean() if segment_size > 0 else 0
    segment_avg_credit = filtered_df["credit_score"].mean() if segment_size > 0 else 0
    
    st.markdown("""
        <div style="background-color: #F8FAFC; padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #E2E8F0;">
            <h3 style="font-size: 1.2rem; margin-top: 0; border: none; padding: 0; color: #2D336B;">Selected Segment Overview</h3>
        </div>
    """, unsafe_allow_html=True)
    
    segment_col1, segment_col2, segment_col3, segment_col4 = st.columns(4)
    
    with segment_col1:
        st.markdown(f"""
            <div class="metric-card" style="border-left-color: #3B82F6;">
                <p class="metric-value">{format_number(segment_size)}</p>
                <p class="metric-label">Segment Size</p>
            </div>
        """, unsafe_allow_html=True)
    
    with segment_col2:
        st.markdown(f"""
            <div class="metric-card" style="border-left-color: #EF4444;">
                <p class="metric-value">{segment_churn_rate:.1f}%</p>
                <p class="metric-label">Segment Churn Rate</p>
            </div>
        """, unsafe_allow_html=True)
    
    with segment_col3:
        st.markdown(f"""
            <div class="metric-card" style="border-left-color: #10B981;">
                <p class="metric-value">${format_number(segment_avg_balance)}</p>
                <p class="metric-label">Avg. Balance</p>
            </div>
        """, unsafe_allow_html=True)
    
    with segment_col4:
        st.markdown(f"""
            <div class="metric-card" style="border-left-color: #8B5CF6;">
                <p class="metric-value">{segment_avg_credit:.1f}</p>
                <p class="metric-label">Avg. Credit Score</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Comparison to overall metrics
    comparison_multiplier = segment_churn_rate / churn_rate if churn_rate > 0 else 0
    risk_level = "Low"
    risk_color = "#10B981"
    
    if comparison_multiplier >= 1.5:
        risk_level = "High"
        risk_color = "#EF4444"
    elif comparison_multiplier >= 1.1:
        risk_level = "Medium"
        risk_color = "#F59E0B"
    
    st.markdown(f"""
        <div style="background-color: #FFF; padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #E2E8F0;">
            <h3 style="font-size: 1.2rem; margin-top: 0; border: none; padding: 0; color: #143D60;">Risk Assessment</h3>
            <div style="display: flex; align-items: center; margin-top: 0.5rem;">
                <div style="width: 20px; height: 20px; border-radius: 50%; background-color: {risk_color}; margin-right: 10px;"></div>
                <span style="font-weight: 600; color: {risk_color};">{risk_level} Risk</span>
                <span style="margin-left: 10px; color: #64748B;">
                    ({comparison_multiplier:.1f}x the average churn rate)
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample data from the segment
    st.markdown("""
        <h3 style="font-size: 1.2rem; margin-top: 1.5rem;">Sample Customer Data</h3>
    """, unsafe_allow_html=True)
    
    if segment_size > 0:
        sample_size = min(10, segment_size)
        st.dataframe(
            filtered_df.sample(sample_size).drop(columns=['age_group', 'credit_score_bin']).reset_index(drop=True),
            use_container_width=True
        )
    else:
        st.info("No customers match the selected criteria.")

# Tab 3: Summary Statistics
with tab3:
    st.markdown("""
        <h2 class="fadeIn">📊 Summary Statistics</h2>
        <p style="color: #64748B;">Detailed statistical analysis of the dataset</p>
    """, unsafe_allow_html=True)
    
    # Dataset overview
    st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.2rem; margin-top: 0; color: #000957;">Dataset Overview</h3>
    """, unsafe_allow_html=True)
    
    overview_col1, overview_col2 = st.columns(2)
    
    with overview_col1:
        st.markdown(f"""
            <table style="width:100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Total Records</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{len(df)}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Features</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{len(df.columns) - 2}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Churn Rate</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{churn_rate:.2f}%</td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
    
    with overview_col2:
        # Calculate gender distribution
        gender_counts = df['gender'].value_counts(normalize=True) * 100
        male_pct = gender_counts.get('Male', 0)
        female_pct = gender_counts.get('Female', 0)
        
        st.markdown(f"""
            <table style="width:100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Male Customers</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{male_pct:.1f}%</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Female Customers</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{female_pct:.1f}%</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; font-weight: 600;">Avg. Credit Score</td>
                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{df['credit_score'].mean():.1f}</td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Numerical statistics
    with st.expander("Numerical Features Statistics", expanded=True):
        st.dataframe(
            df.describe().T.style.format("{:.2f}"),
            use_container_width=True
        )
    
    # Correlation matrix
    st.markdown("""
        <h3 style="font-size: 1.2rem; margin-top: 1.5rem;">Feature Correlation</h3>
        <p style="color: #64748B; font-size: 0.9rem;">
            Correlation between numerical features and churn
        </p>
    """, unsafe_allow_html=True)
    
    # Calculate correlations with churn
    numeric_cols = ['credit_score', 'age', 'tenure', 'balance', 'products_number', 
                   'credit_card', 'active_member', 'estimated_salary', 'churn']
    corr = df[numeric_cols].corr()['churn'].sort_values(ascending=False)
    
    # Create a horizontal bar chart
    fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
    corr_filtered = corr[corr.index != 'churn']  # Remove self-correlation
    colors_corr = ['#3B82F6' if c >= 0 else '#EF4444' for c in corr_filtered]
    
    bars = ax_corr.barh(corr_filtered.index, corr_filtered, color=colors_corr)
    
    # Add value labels
    for i, bar in enumerate(bars):
        label_x = 0.01 if corr_filtered.iloc[i] < 0 else corr_filtered.iloc[i] + 0.01
        ha = 'left' if corr_filtered.iloc[i] < 0 else 'left'
        ax_corr.text(
            label_x, i, 
            f"{corr_filtered.iloc[i]:.3f}", 
            va='center', ha=ha, fontsize=10,
            color='#1E293B'
        )
    
    ax_corr.set_title('Correlation with Churn', fontsize=14, pad=20)
    ax_corr.set_xlabel('Correlation Coefficient', fontsize=12)
    ax_corr.grid(axis='x', alpha=0.3)
    ax_corr.set_axisbelow(True)
    
    # Add vertical line at x=0
    ax_corr.axvline(x=0, color='#94A3B8', linestyle='-', linewidth=1)
    
    # Save and display
    corr_chart_path = save_plot(fig_corr, "correlation_with_churn.png")
    st.image(Image.open(corr_chart_path), use_container_width=True)
    
    # Key numerical insights
    st.markdown("""
        <div style="background-color: #F0FDF4; padding: 1rem; border-radius: 10px; margin-top: 1rem; border-left: 4px solid #10B981;">
            <h3 style="font-size: 1.1rem; color: #065F46; margin-top: 0; border: none; padding: 0;">Key Insights</h3>
            <ul style="margin-bottom: 0; color: #065F46;">
                <li><strong>Active Member Status</strong> has the strongest negative correlation with churn.</li>
                <li><strong>Age</strong> shows a positive correlation with churn, confirming older customers tend to churn more.</li>
                <li><strong>Number of Products</strong> correlates with churn behavior, suggesting product engagement affects retention.</li>
                <li><strong>Salary</strong> has minimal correlation with churn, supporting earlier visual findings.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;">
            <a href="#" style="text-decoration: none;">Terms of Service</a>
            <a href="#" style="text-decoration: none;">Privacy Policy</a>
            <a href="#" style="text-decoration: none;">Support</a>
        </div>
        <p style="color: #000000;">© 2025 BankVision Customer Analytics Platform | Version 2.5.0</p>
        <p style="font-size: 0.8rem; margin-top: 5px; color: #000000;">
            Developed by Abhishek Singh Dikhit | Last updated: """ + current_date + """
        </p>
    </div>
""", unsafe_allow_html=True)