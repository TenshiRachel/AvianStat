import streamlit as st
from helper import get_data

st.set_page_config(
    page_title='Avian Stat',
    layout='wide',
    initial_sidebar_state='expanded'
)

data_functions = ['Overview', 'Drop columns', 'Rename columns', 'Export data',
                  'Handle missing data', 'Edit data', 'Search']
accepted_file_formats = ['csv', 'txt', 'xls', 'xlsx']

uploaded_file = st.sidebar.file_uploader('Upload your data', type=accepted_file_formats)

if uploaded_file is not None:
    file_type = uploaded_file.type.split("/")[1]

    data = get_data(uploaded_file, file_type)

    func_multiselect = st.sidebar.multiselect('What do you want to do with your data?', data_functions,
                                              default=['Overview'])

    st.subheader = 'Dataset preview'
    st.dataframe(data)

    if 'Overview' in func_multiselect:
        # Dataset file details
        pass

    if 'Drop columns' in func_multiselect:
        cols_to_drop = st.multiselect('Select columns to drop', data.columns)
        # Drop columns

    if 'Rename columns' in func_multiselect:
        selected_column = st.selectbox('Select column to rename', options=data.columns)
        rename = st.text_input('Enter new name for {}'.format(selected_column), max_chars=50)
        # Rename columns

    if 'Export data' in  func_multiselect:
        # Download func
        pass

    if 'Handle missing data' in func_multiselect:
        # Remove NaN rows from data or fill with value
        pass

    if 'Edit data' in func_multiselect:
        # Use search func to edit
        selected_column = st.selectbox('Select column to edit in', options=data.columns)
        edit = st.text_input('Enter new value', max_chars=50)
        pass

    if 'Search' in func_multiselect:
        selected_column = st.selectbox('Select column to search in', options=data.columns)
        search = st.text_input('Search in {}'.format(selected_column), max_chars=50)
        pass
