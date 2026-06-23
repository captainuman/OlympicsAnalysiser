import streamlit as st
from streamlit_option_menu import option_menu

from services.data_service import load_data
from utils.constants import PUBLIC_MENU, PRIVATE_MENU
from utils.styles import load_footer

from app_pages.home import show_home
from app_pages.about import show_about
from app_pages.auth import show_auth
from app_pages.olympics_analysis import show_olympics_analysis
from app_pages.prediction import show_prediction
from app_pages.athlete_info import show_athlete_info
from app_pages.sports_analysis import show_sports_analysis
from app_pages.clustering import show_clustering


st.set_page_config(
    page_title="Olympics Data Analysis App",
    page_icon="🏅",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem !important;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)


if "user_logged_in" not in st.session_state:
    st.session_state["user_logged_in"] = False

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""


try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if st.session_state["user_logged_in"]:
    menu_options = PRIVATE_MENU
else:
    menu_options = PUBLIC_MENU

user_menu = option_menu(
    menu_title=None,
    options=menu_options,
    icons=[
        "house",
        "info-circle",
        "box-arrow-in-right",
        "bar-chart-line",
        "graph-up-arrow",
        "person",
        "trophy",
        "diagram-3"
    ][:len(menu_options)],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "10px",
            "background-color": "#eaf3ff",
            "border-radius": "12px",
            "margin-bottom": "10px",
        },
        "icon": {
            "font-size": "18px",
            "padding":"10px"
        },
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "padding": "10px 12px",
            "margin": "0px",
            "font-weight": "600",
        },
        "nav-link-selected": {
            "background-color": "#004d99",
            "color": "white",
            "font-weight": "600",
        },
    }
)

if st.session_state["user_logged_in"]:
    st.sidebar.markdown(f"👤 Logged in as: **{st.session_state['user_name']}**")

    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state["user_logged_in"] = False
        st.session_state["user_name"] = ""
        st.rerun()


st.sidebar.markdown("---")
st.sidebar.info(
    "This app analyzes Olympic history, medal trends, athlete profiles, "
    "sport insights, clustering, and ML-based medal prediction."
)


if user_menu == "Home Page":
    show_home()

elif user_menu == "About Project":
    show_about()

elif user_menu == "Login / Register":
    show_auth()

elif user_menu == "Olympics Analysis":
    show_olympics_analysis(df)

elif user_menu == "Olympic Prediction":
    show_prediction(df)

elif user_menu == "Athlete Information":
    show_athlete_info(df)

elif user_menu == "Sports Analysis":
    show_sports_analysis(df)

elif user_menu == "Athlete Clustering":
    show_clustering(df)

load_footer()