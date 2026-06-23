import streamlit as st
import plotly.express as px
from helper import run_kmeans_on_athletes


def show_clustering(df):

    if not st.session_state["user_logged_in"]:
        st.warning("🚫 Please log in to access this page.")
        st.stop()

    st.title("🧬 Athlete Clustering Analysis")

    k = st.slider("Select Number of Clusters", 2, 8, 3)

    clustered_df, kmeans = run_kmeans_on_athletes(df, k)

    fig = px.scatter(
        clustered_df,
        x="Height",
        y="Weight",
        color="Cluster",
        title="Athlete Clusters by Height and Weight"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Clustered Athlete Data")
    st.dataframe(clustered_df.head(100))