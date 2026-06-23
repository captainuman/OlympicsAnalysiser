import streamlit as st
import pandas as pd
from datetime import datetime

def show_athlete_info(df):

    st.title("🔎 Athlete Detailed Profile")

    athlete_input = st.text_input(
        "Enter Athlete Name (Full or Partial)"
    ).strip()

    if athlete_input:
        search_keywords = athlete_input.lower().split()

        def match_athlete(name):
            name_tokens = str(name).lower().split()
            return all(any(keyword in token for token in name_tokens) for keyword in search_keywords)

        matched_athletes = df[df['Name'].apply(match_athlete)]

        if matched_athletes.empty:
            st.warning("No athlete found with that name.")
        else:
            unique_names = matched_athletes['Name'].unique().tolist()
            selected_profile = st.selectbox("Select Athlete", unique_names)

            athlete_df = matched_athletes[matched_athletes['Name'] == selected_profile]

            # Basic Info
            st.subheader(f"👤 Profile till 2020: {selected_profile}")
            sex = athlete_df['Sex'].mode()[0]
            region = athlete_df['region'].mode()[0]
            latest_age = athlete_df['Age'].dropna().max()
            latest_year = athlete_df['Year'].max()
            current_year = datetime.now().year
            estimated_age = int(latest_age + (current_year - latest_year))
            st.markdown(f"- **Sex**: {sex}")
            st.markdown(f"- **Region**: {region}")
            st.markdown(f"- **Age (most recent)**: {(estimated_age) if not pd.isna(estimated_age) else 'Unknown'}")

            # Olympic participation
            years = sorted(athlete_df['Year'].unique())
            st.markdown(f"- **Years Participated**: {years}")
            st.markdown(f"- **Games Played**: {len(years)}")

            sports = sorted(athlete_df['Sport'].dropna().unique())
            st.markdown(f"- **Sports Played**: {sports}")

            events = sorted(athlete_df['Event'].dropna().unique())
            st.markdown(f"- **Events Competed In**: {events}")

            # Medals
            medals = athlete_df['Medal'].value_counts()
            gold = medals.get("Gold", 0)
            silver = medals.get("Silver", 0)
            bronze = medals.get("Bronze", 0)
            total = gold + silver + bronze

            st.markdown("### 🏅 Medals Won")
            st.markdown(f"- 🥇 Gold: **{gold}**")
            st.markdown(f"- 🥈 Silver: **{silver}**")
            st.markdown(f"- 🥉 Bronze: **{bronze}**")
            st.markdown(f"- 🎖️ Total: **{total}**")

            # Raw Participation Records
            with st.expander("📜 Show All Records for This Athlete"):
                st.dataframe(athlete_df.sort_values(by='Year'))
