import streamlit as st
import plotly.express as px
import pandas as pd

def sport_analysis(df, selected_sport):
    """
    Analyzes data for a single sport and displays relevant information.

    Args:
        df (pd.DataFrame): The main Olympics DataFrame.
        selected_sport (str): The name of the sport to analyze.
    """
    st.header(f"Analysis for {selected_sport}")

    # 1. Medals Over Time for the Sport
    sport_df = df[df['Sport'] == selected_sport]
    medal_over_time = sport_df.groupby('Year')['Medal'].count().reset_index()
    fig_medals = px.line(medal_over_time, x='Year', y='Medal', title=f"Medal Trend for {selected_sport} Over Time")
    st.plotly_chart(fig_medals)

    # 2. Top Participating Countries
    top_countries = sport_df['region'].value_counts().head(10).reset_index()
    top_countries.columns = ['Country', 'Count']
    fig_countries = px.bar(top_countries, x='Country', y='Count', title=f"Top 10 Participating Countries in {selected_sport}")
    st.plotly_chart(fig_countries)

    # 3. Age Distribution of Athletes
    fig_age = px.histogram(sport_df, x='Age', title=f"Age Distribution of Athletes in {selected_sport}")
    st.plotly_chart(fig_age)

    # 4. Gender Participation
    gender_counts = sport_df['Sex'].value_counts().reset_index()
    gender_counts.columns = ['Sex', 'Count']
    fig_gender = px.pie(gender_counts, values='Count', names='Sex', title=f"Gender Participation in {selected_sport}")
    st.plotly_chart(fig_gender)

    # 5. Most Successful Athletes in the Sport
    st.subheader(f"Most Successful Athletes in {selected_sport}")
    athlete_medal_counts = sport_df.groupby('Name')['Medal'].count().reset_index()
    athlete_medal_counts = athlete_medal_counts.sort_values(by='Medal', ascending=False).head(10)
    athlete_medal_counts.columns = ['Athlete', 'Medal Count']
    st.table(athlete_medal_counts)

    # 6. Medals Won by Each Country
    country_medal_counts = sport_df.groupby('region')['Medal'].count().reset_index()
    country_medal_counts = country_medal_counts.sort_values(by='Medal', ascending=False)
    country_medal_counts.columns = ['Country', 'Medal Count']
    fig_country_medals = px.bar(country_medal_counts, x='Country', y='Medal Count', title=f"Medals Won by Each Country in {selected_sport}")
    st.plotly_chart(fig_country_medals)

def show_sports_analysis(df):

    if not st.session_state["user_logged_in"]:
        st.warning("🚫 Please log in to access this page.")
        st.stop()

    st.title("🏅 Sport-Specific Analysis")

    sport_list = sorted(df["Sport"].unique().tolist())
    selected_sport = st.selectbox("Select a Sport", sport_list)

    sport_analysis(df, selected_sport)