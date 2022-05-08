import datetime

import app.login
import streamlit as st


def sidebar_run():
    with st.sidebar:
        app.login.run_app()
    return ""


def mainpage_run():
    st.write("""## Welcome page""")
    return ""
