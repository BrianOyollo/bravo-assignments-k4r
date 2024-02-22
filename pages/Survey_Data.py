import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from authentication import auth

st.set_page_config(
    page_title='K4R',
    layout='wide'
)

authenticator = auth.authenticate_user()
name, authentication_status, username = authenticator.login()
if authentication_status:
    c1,c2 = st.columns([.9,0.1])
    with c2:
        authenticator.logout('Logout', 'main')

    st.header('Survey Data')
    st.subheader(':green[Kenya4Resilience Consortium]')

    @st.cache_data(show_spinner=':blue[Loading survey data...]')
    def load_raw_data(file_path, sheet_name=None):
        raw_data = pd.read_excel(file_path)
        raw_data.astype({'phonenumber':'str'})
        return raw_data

    @st.cache_data(show_spinner=':blue[Loading survey data...]')
    def load_cleaned_data(file_path, sheet_name=None):
        cleaned_df = pd.read_excel(file_path)
        # cleaned_df.astype({'phonenumber':'str'})
        return cleaned_df
    
    raw_data=load_raw_data('raw_labeled_data.xlsx')
    cleaned_data=load_cleaned_data('cleaned_data.xlsx')

    option = st.radio("Select Data to Display", ['Raw Data', 'Cleaned Data'])
    if option == 'Raw Data':
        st.data_editor(raw_data, key='raw_data', use_container_width=True)
    elif option == 'Cleaned Data':
        st.data_editor(cleaned_data, key='cleaned_data', use_container_width=True)

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please login to view this page')