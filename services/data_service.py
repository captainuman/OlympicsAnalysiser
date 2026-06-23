import pandas as pd
import streamlit as st
import preprocessor
from utils.constants import DATA_PATH, REGION_PATH


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="latin1")
    region_df = pd.read_csv(REGION_PATH, encoding="latin1")

    df = preprocessor.preprocess(df, region_df)

    return df