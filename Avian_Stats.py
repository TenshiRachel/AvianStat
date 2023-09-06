import streamlit as st
import pandas as pd
from helper import clean_plane_data

st.set_page_config(
    page_title='Avian Stat',
    layout='wide',
    initial_sidebar_state='expanded'
)

data = pd.read_csv('./Airplane_Crashes_Since_1908.csv')

data = clean_plane_data(data)

st.header = 'Analysis of plane crash statistics'
