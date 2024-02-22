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

    st.title(":green[DashBoard]")

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please login to view this page')