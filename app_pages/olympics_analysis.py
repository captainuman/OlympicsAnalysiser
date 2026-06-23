import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import helper


def show_olympics_analysis(df):
    if not st.session_state["user_logged_in"]:
        st.warning("🚫 Please log in to access this page.")
        st.stop()

    analysis_menu = st.sidebar.radio(
        "Select an option",
        ("Medal Tally", "Overall-Analysis", "Country-wise Analysis")
    )

    if analysis_menu == "Medal Tally":
        st.sidebar.header("Medal Tally")

        years, country = helper.country_year_list(df)

        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_country = st.sidebar.selectbox("Select Country", country)

        medal_tally_df = helper.fetch_medal_tally(df, selected_year, selected_country)

        title = "Overall Tally"
        if selected_year != "Overall" and selected_country == "Overall":
            title = f"Medal Tally in {selected_year} Olympics"
        elif selected_year == "Overall" and selected_country != "Overall":
            title = f"{selected_country} Overall Performance"
        elif selected_year != "Overall" and selected_country != "Overall":
            title = f"{selected_country} in {selected_year} Olympics"

        st.title(title)
        st.table(medal_tally_df)

        csv = medal_tally_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Medal Tally CSV",
            data=csv,
            file_name="medal_tally.csv",
            mime="text/csv"
        )

    if analysis_menu == "Overall-Analysis":
        st.title("📊 Overall Olympic Statistics")

        editions = df["Year"].nunique()
        cities = df["City"].nunique()
        sports = df["Sport"].nunique()
        events = df["Event"].nunique()
        athletes = df["Name"].nunique()
        nations = df["region"].nunique()

        st.markdown("### 📌 Key Olympic Statistics")

        col1, col2, col3 = st.columns(3)
        col1.metric("🏟️ Editions", editions)
        col2.metric("🌆 Host Cities", cities)
        col3.metric("🏅 Sports", sports)

        col4, col5, col6 = st.columns(3)
        col4.metric("🎯 Events", events)
        col5.metric("🌍 Nations", nations)
        col6.metric("🏃 Athletes", athletes)

        st.divider()

        st.title("🌍 World Medal Map")

        map_df = df.dropna(subset=["Medal"])
        map_df = map_df.drop_duplicates(
            subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
        )

        country_medals = (
            map_df.groupby("region")
            .count()["Medal"]
            .reset_index()
            .rename(columns={"region": "Country", "Medal": "Total Medals"})
        )

        fig = px.choropleth(
            country_medals,
            locations="Country",
            locationmode="country names",
            color="Total Medals",
            hover_name="Country",
            title="Total Olympic Medals by Country"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.title("📈 Trends Over Time")

        nations_over_time = helper.data_over_time(df, "region")
        fig = px.line(nations_over_time, x="Edition", y="region", title="Participating Nations Over Time")
        st.plotly_chart(fig, use_container_width=True)

        events_over_time = helper.data_over_time(df, "Event")
        fig = px.line(events_over_time, x="Edition", y="Event", title="Events Over Time")
        st.plotly_chart(fig, use_container_width=True)

        athletes_over_time = helper.data_over_time(df, "Name")
        fig = px.line(athletes_over_time, x="Edition", y="Name", title="Athletes Over Time")
        st.plotly_chart(fig, use_container_width=True)

        st.title("Men vs Women Participation Over the Years")
        final = helper.men_vs_women(df)
        fig = px.line(final, x="Year", y=["Male", "Female"])
        st.plotly_chart(fig, use_container_width=True)

        st.title("🎯 Events per Sport Over Time")
        fig, ax = plt.subplots(figsize=(20, 20))
        data = df.drop_duplicates(["Year", "Sport", "Event"])
        heatmap_data = data.pivot_table(
            index="Sport",
            columns="Year",
            values="Event",
            aggfunc="count"
        ).fillna(0).astype(int)
        sns.heatmap(heatmap_data, annot=True, ax=ax)
        st.pyplot(fig)

        st.title("🏆 Most Successful Athletes")
        sport_list = sorted(df["Sport"].unique().tolist())
        sport_list.insert(0, "Overall")
        selected_sport = st.selectbox("Select a Sport", sport_list)
        st.table(helper.most_successful(df, selected_sport))

    if analysis_menu == "Country-wise Analysis":
        st.title("🌍 Country-wise Analysis")

        country_list = sorted(df["region"].dropna().unique().tolist())
        selected_country = st.sidebar.selectbox("Select Country", country_list)

        country_df = helper.yearwise_medal_tally(df, selected_country)
        fig = px.line(
            country_df,
            x="Year",
            y="Medal",
            title=f"{selected_country} - Medal Tally Over Years"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.title(f"{selected_country} - Top Sports")
        heatmap = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(heatmap, annot=True, ax=ax)
        st.pyplot(fig)

        st.title(f"Top 10 Athletes from {selected_country}")
        st.table(helper.most_successful_countrywise(df, selected_country))