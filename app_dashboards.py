"Dashboards demos"

import datetime
from pathlib import Path

import streamlit as st

import app.login
import page.dashboards
import page.welcome

LOGO_LOC = "./media/ADAO_logo.png"

app.login.initiate_session_state()

st.set_page_config(
    page_title="ADAO - Dashboards",
    page_icon=LOGO_LOC,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # "Get Help": "https://www.apps.adao.tech"
    },
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():

    st.sidebar.image(image=LOGO_LOC, width=300)
    # pages
    page_names = ["Welcome", "Demo - dashboards"]
    page_apps = [page.welcome, page.dashboards]

    page_map = dict(zip(page_names, page_apps))
    page_selected = st.sidebar.selectbox("Menu", page_names)
    st.sidebar.markdown("---")

    with st.spinner("Loading"):
        with st.sidebar:
            if not app.login._is_auth():
                if page_selected != "Welcome":
                    st.warning(f"Please login to access {page_selected}")
                st.write(page_map["Welcome"].sidebar_run())
            else:
                st.write(page_map[page_selected].sidebar_run())

            st.markdown("---")
            st.info("INFORMATION ABOUT APP")

    # st.markdown("# ADAO Model Portal")
    with st.spinner(f"Loading {page_selected}"):
        if not app.login._is_auth():
            if page_selected != "Welcome":
                st.warning(f"Please login to access {page_selected}")
            st.write(page_map["Welcome"].mainpage_run())
        else:
            st.write(page_map[page_selected].mainpage_run())

    st.markdown("---")

    st.write(
        """### Contact

 Contact us:

 - Form: [Contact form](https://docs.google.com/forms/d/e/1FAIpQLSeuMiVF7f0XVMQ8C-9jntlQU_lBzX0J5dymg1yLt7Y0QxUN_Q/viewform?usp=sf_link)

 - Email: <contact@adao.tech>
        """
    )

    st.write(
        """### Disclaimer
    This software is presented "as-is" and the user accepts this condition
    before using it.  In its current form it is a Demo and no representation is
    given as to performance nor compliance. Also, no warranties are offered as
    to the software's functionality. The software can be used for demonstration
    purposes only.

    The software is subject to copyrights and no license is offered as part of
    the demonstration offered here. Users are solely responsible for damages of
    any kind that may ensue from using this software in any way beyond this
    demonstration."""
    )  # TODO


if __name__ == "__main__":
    main()
