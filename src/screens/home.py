import streamlit as st
from src.database.db import user_login_db, check_user_exist, create_user_account
from src.ui.layout import layout

def login():
    layout()
    st.markdown(
        """
        <div class= "icon">📔</div>
        <div class="main-heading">DocuMind AI</div>
        <div class="sub-heading">Your AI-powered document assistant</div> 
        """,
        unsafe_allow_html=True
    )
    
    with st.container(key="main-container"):
        st.markdown(
            """
            <div class="title">
                Welcome
            </div>

            <div class="subtitle">
                Login to access your personalized document assistant.
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            '<div class="input-label">Email</div>',
            unsafe_allow_html=True
        )

        email_id = st.text_input(
            "Email",
            placeholder="Enter your Email",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="input-label password-label">Password</div>',
            unsafe_allow_html=True
        )

        password1 = st.text_input(
            "Password1",
            placeholder="Enter your Password",
            type="password",
            label_visibility="collapsed"
        )
        col1,col2, col3= st.columns([3,3,3])
        with col2:
            login_button = st.button(
                "Login →",
                key="login_btn",
                width='stretch'
            )

        if login_button:
            
            if not email_id or not password1:
                st.error("All fields are required to enter.")

            else:
                user= user_login_db(email_id, password1)
                if user==None:
                    st.error("User does not exist, please register first")
                elif user==False:
                    st.error("Invalid password, please try again")
                else:
                    st.session_state.user_data= user
                    st.session_state.user_login_type= "dashboard"
                    st.success("Login successful!")

                    #st.toast("Welcome back!", icon="🎉")
                    import time 
                    time.sleep(1)
                    st.rerun()
            
        st.markdown(
            """
            <div class="divider">
                <span>OR</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="register-text" style="text-align: center;">
                Don't have an account?
            </div>
            """,
            unsafe_allow_html=True
        )

        col1,col2, col3= st.columns([3,3,3])
        with col2: 
            if st.button("Register",key="register_btn1", width="stretch"):
                st.session_state.user_login_type = "register"

def register():
    layout()
    st.markdown(
        """
        <div class= "icon">📔</div>
        <div class="main-heading">DocuMind AI</div>
        <div class="sub-heading">Your AI-powered document assistant</div> 
        """,
        unsafe_allow_html=True
    )

    with st.container(key="main-container"):
        st.markdown(
            """
            <div class="title">
                Create Account
            </div>

            <div class="subtitle">
                Register to access your personalized document assistant.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="input-label">Name</div>',
            unsafe_allow_html=True
        )

        name = st.text_input(
            "Name",
            placeholder="Enter your Name",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="input-label">Email</div>',
            unsafe_allow_html=True
        )

        email_id = st.text_input(
            "Email",
            placeholder="Enter your Email",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="input-label password-label">Password</div>',
            unsafe_allow_html=True
        )

        password = st.text_input(
            "Password",
            placeholder="Enter your Password",
            type="password",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="input-label password-label">Confirm Password</div>',
            unsafe_allow_html=True
        )

        confirm_password = st.text_input(
            "Confirm Password",
            placeholder="Confirm your Password",
            type="password",  
            label_visibility="collapsed"
        )

        col1,col2, col3= st.columns([3,3,3])
        with col2:
            register_button = st.button(
                "Register →",
                key="register_btn",
                width='stretch'
            )

        if register_button:
            if not name or not email_id or not password or not confirm_password:
                st.error("All fields are required to register.")
            elif password != confirm_password:
                st.error("Password does not match.")
            else:
                if check_user_exist(email_id):
                    st.error("User already exists, please login.")
                else:
                    user= create_user_account(name, email_id, password)
                    if user:
                        st.success("Account created successfully! Please login.")
                        st.session_state.user_login_type = "login"
                        st.rerun()
                    else:
                        st.error("Error creating account. Please try again.")


