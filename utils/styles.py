import streamlit as st


def load_sidebar_branding():
    st.sidebar.markdown(
        """
        <h2 style='text-align: center; color: #004d99;'>
            🏅 Olympics App
        </h2>
        """,
        unsafe_allow_html=True
    )


def load_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center'>
            <h4>🏅 Olympics Data Analysis & Medal Prediction App</h4>
            <p>Built with Streamlit, Plotly, Scikit-Learn and XGBoost</p>
            <p>Developed by Numan</p>
        </div>
        """,
        unsafe_allow_html=True
    )