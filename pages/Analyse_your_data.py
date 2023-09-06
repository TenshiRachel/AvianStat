import streamlit as st
from helper import get_data

st.set_page_config(
    page_title='Avian Stat',
    layout='wide',
    initial_sidebar_state='expanded'
)

data_functions = ['Overview', 'Drop columns', 'Rename columns', 'Export data', 'Handle missing data']
accepted_file_formats = ['csv', 'txt', 'xls', 'xlsx']

uploaded_file = st.sidebar.file_uploader('Upload your data')

if uploaded_file is not None:
    file_type = uploaded_file.type.split("/")[1]

    data = get_data(uploaded_file, file_type)

    st.sidebar.multiselect('What do you want to do with your data?', data_functions, default=['Overview'])

    st.subheader = 'Dataset preview'
    st.dataframe(data)
