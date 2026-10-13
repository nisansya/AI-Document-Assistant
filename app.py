import streamlit as st
from src.screens.home import login, register
from src.screens.dashboard import dashboard

if "user_login_type" not in st.session_state:
    st.session_state.user_login_type= "login"

if st.session_state.user_login_type=="login":
    login()

elif st.session_state.user_login_type=="register":
    register()

else:
    dashboard()

