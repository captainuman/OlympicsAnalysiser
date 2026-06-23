import streamlit as st
import streamlit.components.v1 as components

def show_home():
    st.markdown(
        """
        <h1 style='text-align: center; color: #004d99;'>
            🏅 Olympics Data Analysis & Medal Prediction App
        </h1>
        <p style='text-align: center; font-size:18px;'>
            Interactive dashboard for Olympic history, country analysis, athlete insights,
            sport-wise trends, and machine learning medal prediction.
        </p>
        """,
        unsafe_allow_html=True
    )

    html_code = """
    <div style='text-align:center; padding:40px;'>
        <h2>Explore Olympic History</h2>
        <p>Analyze results, athletes, countries, sports and predict future outcomes.</p>
    </div>
    """

    components.html(html_code, height=250)