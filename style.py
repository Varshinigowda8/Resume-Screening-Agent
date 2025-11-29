def inject_custom_css():
    import streamlit as st
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f7fa;
        }
        h1 {
            color: #4B8BBE;
            font-size: 42px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
