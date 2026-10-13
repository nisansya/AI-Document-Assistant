import streamlit as st

def layout():
    st.set_page_config(
        page_title= "DocuMind AI",
        page_icon= "📔",
        layout= "wide",
        initial_sidebar_state= "expanded"
    )

    st.markdown(
        """
        <style>

        /* ---------------- GLOBAL ---------------- */

            .stApp {
                background: #07111f !important;
                color: #f1f5f9 !important;
            }

            #MainMenu, footer, header {
                visibility: hidden;
            }
            
            .main{
                background-color: #0f1117 !important;
            }

            [data-testid="stHeader"]{
                backgound: transparent !important;
            }

            .block-container{
                padding-top: 2rem !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
                max-width: 1500px !important;
            }

            /* =====================================================
            LOGIN PAGE
            ===================================================== */

            .st-key-main-container {
                background-color: #ob1a2c !important;
                min-height: 800px !important;
                border: 1px solid #1f3b5d !important;
                padding: 40px !important;
                border-radius: 0px 18px 18px 0px !important;
                box-sizing: border-box !important;
            }

            .main-heading{
                font-size: 50px !important;
                font-weight: 750 !important;
                color: #F7F7FA !important;
                margin-bottom: 7px !important;
                text-align: center !important;
            }

            .sub-heading{
                font-size: 25px !important;
                color: #8C94A5 !important;
                text-align: center !important;
            }

            .icon{
                text-align: center !important;
                size: 30px !important;
            }

            .title {
                font-size: 38px !important;
                font-weight: 700 !important;
                color: #17233c !important;
                font-family: 'Oswald', sans-serif !important;
                margin-bottom: 35px !important;
                text-align: center !important;
            }

            .subtitle{
                color: #8E96A8 !important;
                font-size: 19px !important;
                margin-left: 54px !important;
                margin-top: 7px !important;
                margin-bottom: 28px !important;
                text-align: center !important;
            }
            
            .password-label {
                margin-top: 18px !important;
            }

        
            .divider {
                display: flex !important;
                align-items: center !important;
                text-align: center !important;
                margin: 28px 0px !important;
                color: #8b96a8 !important;
                font-size: 14px !important;
            }

            .divider::before,
            .divider::after {
                content: '' !important;
                flex: 1 !important;
                height: 1px !important;
                background: #e1e5eb !important;
            }

            .divider span {
                padding: 0 15px !important;
            }

            /* =====================================================
            DASHBOARD
            ===================================================== */
            

            [data-testid="stSidebar"]{
                background-colr: #151922 !important;
                border-right: 1px solid #252B38 !important;
            }

            [data-testid="stSidebar"] > div{
                padding-top: 1.5rem !important;
            }
            

            .main-title{
                font-size: 34px !important;
                font-weight: 700 !important;
                color: #FFFFFF !important;
            }

            .sub-title{
                color: #8E96A8 !important;
                font-size: 19px !important;
                margin-left: 54px !important;
                margin-top: 7px !important;
                margin-bottom: 28px !important;
            }

            .sidebar-heading{
                color: #858EA1 !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                letter-spacing: 1px !important;
                margin-top: 20px !important;
                margin-bottom: 12px !important;
                text-transform: uppercase !important;
            }

            .chat-heading{
                color: #858EA1 !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                letter-spacing: 1px !important;
                margin-top: 20px !important;
                margin-bottom: 12px !important;
                text-transform: uppercase !important;
            }

            .document-card{
                background: #1B202B !important;
                border: 1px solid #282F3D !important;
                border-radius: 10px !important;
                padding: 11px !important;
                margin-bottom: 8px !important;
            }

            .document-name{
                color: #E8EAFO !important;
                font-size: 17px !important;
                font-weight: 500px !important;
            }

            .st-key-right-panel {
                background-color: #ob1a2c !important;
                min-height: 800px !important;
                border: 1px solid #1f3b5d !important;
                padding: 40px !important;
                border-radius: 0px 18px 18px 0px !important;
                box-sizing: border-box !important;
            }

            .main-heading{
                font-size: 50px !important;
                font-weight: 750 !important;
                color: #F7F7FA !important;
                margin-bottom: 7px !important;
            }

            .sub-heading{
                font-size: 25px !important;
                color: #8C94A5 !important;
            }

            .para{
                font-size: 18px !important;
                color: white !important;
                margin-bottom: 20px !important;
                            
            }

            .input-label {
                font-size: 13px !important;
                font-weight: 600 !important;
                color: #AAB2CO !important;
                font-family: 'Outfit', sans-serif !important;
                margin-bottom: 10px !important;
                margin-top: 60px !important;
            }

            div[data-baseweb="input"]{
                border: 1px solid #303746 !important;
                background: #1A1F29 !important;
                border-radius: 14px !important;
                min-height: 48px !important;
                margin-top: 50px !important;
            }

            .mode-title {
                color: #AAB2C0 !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                margin-top: 25px !important;
                margin-bottom: 12px !important;
            }

            .mode-card {
                background: #171C25 !important;
                border: 1px solid #282F3D !important;
                border-radius: 12px !important;
                padding: 15px !important;
                min-height: 95px !important;
            }

            .mode-icon {
                font-size: 22px !important;
                margin-bottom: 7px !important;
            }

            .mode-name {
                color: #F2F3F6 !important;
                font-size: 14px !important;
                font-weight: 650 !important;
            }

            .mode-description {
                color: #777F90 !important;
                font-size: 11px !important;
                margin-top: 5px !important;
                line-height: 1.4 !important;
            }


            /* =====================================================
            SECTION
            ===================================================== */

            .section-header {
                display: flex !important;
                align-items: center !important;
                gap: 9px !important;
                margin-top: 30px !important;
                margin-bottom: 12px !important;
            }

            .section-icon {
                font-size: 20px !important;
            }

            .section-title {
                font-size: 17px !important;
                font-weight: 650 !important;
                color: #F3F4F7 !important;
            }


            /* =====================================================
            RESPONSE CARD
            ===================================================== */

            .response-card {
                background: #171C25 !important;
                border: 1px solid #2A3140 !important;
                border-radius: 14px !important;
                padding: 20px !important;
                line-height: 1.7 !important;
                color: #CDD2DC !important;
                font-size: 14px !important;
            }

            .response-label {
                color: #8F97A8 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                margin-bottom: 10px !important;
            }


            /* =====================================================
            SOURCE CARDS
            ===================================================== */

            .source-card {
                background: #171C25 !important;
                border: 1px solid #282F3D !important;
                border-radius: 10px !important;
                padding: 13px !important;
                margin-bottom: 8px !important;
            }

            .source-name {
                color: #E8EAF0 !important;
                font-size: 13px !important;
                font-weight: 600 !important;
            }

            .source-page {
                color: #747D90 !important;
                font-size: 11px !important;
                margin-top: 4px !important;
            }


            /* =====================================================
            BUTTONS
            ===================================================== */

            .stButton > button {
                width: 100% !important;
                border-radius: 9px !important;
                border: 1px solid #303747 !important;
                background: #1B202B !important;
                color: #DCE0E8 !important;
                font-size: 12px !important;
                font-weight: 500 !important;
                transition: 0.2s !important;
            }

            .stButton > button:hover {
                border-color: #6C63FF !important;
                color: #FFFFFF !important;
            }


            /* =====================================================
            FILE UPLOADER
            ===================================================== */

            [data-testid="stFileUploader"] {
                background: #1B202B !important;
                border-radius: 10px !important;
                border: 1px solid #282F3D !important;
            }

            [data-testid="stFileUploader"] section {
                background: transparent !important;
                border: none !important;
            }

            .active-mode{
                margin-top: 18px !important;
                color: #8F97A8; !important
                font-size: 12px !important;
            }

            span{
                background: #242044 !important;
                color: #A9A2FF !important;
                padding: 5px 10px !important;
                border-radius: 15px !important;
            }

            

        """,
        unsafe_allow_html= True
    )