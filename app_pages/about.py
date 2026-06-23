import streamlit as st

def show_about():

    st.title("🏅 Olympics Data Analysis & Medal Prediction Platform")

    st.markdown("""
    ### Overview

    The Olympics Data Analysis & Medal Prediction Platform is an interactive analytics
    application built using Streamlit, Machine Learning, and Data Visualization tools.

    The platform allows users to explore over a century of Olympic Games history,
    analyze athlete and country performance, visualize trends, and predict medal outcomes
    using machine learning models.

    ---

    ## 🎯 Project Objectives

    - Analyze historical Olympic Games data
    - Explore country-wise and athlete-wise performance
    - Visualize Olympic participation trends
    - Identify patterns in sports and medal distributions
    - Predict athlete medal outcomes using Machine Learning
    - Cluster athletes based on physical attributes and performance

    ---

    ## 🚀 Key Features

    ### 📊 Olympics Analysis
    - Interactive Medal Tally Dashboard
    - Country-wise Performance Analysis
    - Olympic Statistics Dashboard
    - Participation Trends Over Time
    - Men vs Women Participation Analysis
    - World Medal Distribution Map

    ### 🏃 Athlete Analytics
    - Athlete Profile Search
    - Career Performance Analysis
    - Medal History
    - Event Participation Statistics
    - Estimated Current Age Calculation

    ### 🏆 Sports Analysis
    - Sport-specific Performance Analysis
    - Event-wise Statistics
    - Historical Participation Trends
    - Top Athletes by Sport

    ### 🤖 Machine Learning
    - Athlete Medal Prediction
    - Country Medal Prediction
    - Random Forest Models
    - Logistic Regression Models
    - XGBoost Models

    ### 🧬 Clustering & Analytics
    - K-Means Athlete Clustering
    - Height vs Weight Analysis
    - Athlete Group Identification

    ---

    ## 📈 Dataset Information

    The project uses historical Olympic Games datasets containing:

    - Athlete Information
    - Countries and Regions
    - Olympic Events
    - Sports Categories
    - Medal Records
    - Participation History

    Data covers more than 120 years of Olympic Games history.

    ---

    ## 🛠️ Technologies Used

    ### Backend & Analytics
    - Python
    - Pandas
    - NumPy

    ### Machine Learning
    - Scikit-Learn
    - XGBoost

    ### Data Visualization
    - Plotly
    - Matplotlib
    - Seaborn

    ### Application Framework
    - Streamlit

    ---

    ## 📌 Project Architecture

    The application follows a modular architecture:

    - app.py → Main Application
    - app_pages/ → UI Pages
    - services/ → Business Logic
    - utils/ → Configuration & Styling
    - helper.py → Analytics Functions
    - preprocessor.py → Data Cleaning Pipeline

    ---

    ## 👨‍💻 Developer

    **Numan**

    Data Analytics | Machine Learning | Python Development

    This project demonstrates practical skills in:

    - Data Analysis
    - Data Visualization
    - Machine Learning
    - Software Engineering
    - Dashboard Development
    - Streamlit Application Development

    ---

    ## 🌟 Future Enhancements

    - Olympic Medal Forecasting
    - Deep Learning Models
    - Real-Time Sports Data Integration
    - User Accounts & Profiles
    - Advanced Predictive Analytics
    - Cloud Deployment
    """)