"""This module contains the logic for sign in, login, logout and other basic
functionality to authenticate users. It is not aimed to be a secure solution.

"""

import datetime
import hashlib
import json

import streamlit as st

LOGIN_DB = "./app_data/login_app_db.json"

# Reset password
# >>> pwd = "guest"
# >>> key = hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), salt.encode("utf-8"), 100_000).hex()
# >>> base_db["alejandro"] = {"user":"alejandro", "salt" : "12345678"*4, "pwd_key" : key}
# >>> with open("./app_data/login_app_db.json", "w") as file:
# >>>	json.dump(base_db, file, indent=4)


def initiate_session_state():
    # Set all relevant fields:  <24-09-21, yourname> #
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = ""
    if "password" not in st.session_state:
        st.session_state["pwd_key"] = ""
    if "bytes_data" not in st.session_state:
        st.session_state["bytes_data"] = None
    if "login_date" not in st.session_state:
        st.session_state["login_date"] = None
    if "predictions" not in st.session_state:
        st.session_state["predictions"] = None

    pass


def login_sidebar(sidebar):
    with st.sidebar:
        if not _is_auth():
            st.sidebar.markdown("Please login in the welcome page")
        else:
            sidebar


def login_main(main):
    if not _is_auth():
        st.markdown("### Please login in the welcome page")
    else:
        main()


def run_app():
    """Creates the signin prompt with logout. Uses st.session_state from
    streamlit.

    The following variables are used in st.session_state["user_info"]:
        user:
        pwd_key:
        pwd_salt:
        is_authenticated:
    """

    if _is_auth():
        st.markdown(
            f"""
**User**: {st.session_state["user"]}

**Login date**: {st.session_state["login_date"]}
"""
        )

        if st.button("Sign out"):
            _do_logout()
            st.experimental_rerun()

        with st.expander("Change password"):
            with st.form(key="change_password_form"):
                pwd_check = st.text_input("Current password", value="", type="password")

                _correct_pwd = _is_correct_pwd(
                    pwd_check, st.session_state["user_info"]["salt"]
                )
                pwd_1 = st.text_input("Password:", value="", type="password")
                pwd_2 = st.text_input("Password (again):", value="", type="password")
                click_change_pwd = st.form_submit_button("Change password")

            if click_change_pwd:
                if pwd_1 == pwd_2 and _correct_pwd:
                    _change_pwd(pwd_1, st.session_state["user_info"]["salt"])
                    st.success("Password changed successfully")

                else:
                    st.warning(
                        "Current password is wrong or new passwords do not match"
                    )

        if st.session_state["user"] == "admin":
            with st.expander("Add/change user"):
                with st.form(key="add_user"):
                    user = st.text_input("User:", value="")
                    pwd = st.text_input("Password:", value="", type="password")
                    salt = st.text_input("Salt:", value="12345678" * 4)
                    click_add_user = st.form_submit_button("Add user")

                if click_add_user:
                    _add_user(user, pwd, salt)
                    st.success("User/change added")

    else:
        st.markdown("### Please Login")
        with st.form(key="login_form"):
            user = st.text_input("User:", value="")
            pwd = st.text_input("Password:", value="", type="password")
            submit_click = st.form_submit_button("Login")

        if submit_click:
            with open(LOGIN_DB, "r") as json_db:
                db = json.load(json_db)
                _user_exist = user in db

            if _user_exist:
                st.session_state["user_info"] = db[user]
                _correct_pwd = _is_correct_pwd(
                    pwd, st.session_state["user_info"]["salt"]
                )

                if _correct_pwd:
                    _do_login(user, pwd)
                    st.experimental_rerun()

                else:
                    st.warning("Incorrect user or password")

            else:
                st.warning("User does not exist")
    return ""


def _is_auth():
    """Determines if a user is authenticated."""
    # return user == "guest" and pwd == "guest"

    return st.session_state.get("is_authenticated", False)


def _pwd2key(pwd: str, salt) -> str:
    key = hashlib.pbkdf2_hmac(
        "sha256", pwd.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
    return key


def _is_correct_pwd(pwd: str, salt: str):
    new_key = _pwd2key(pwd, salt)
    return st.session_state["user_info"].get("pwd_key", None) == new_key


def _change_pwd(pwd, salt):
    new_key = _pwd2key(pwd, salt)
    st.session_state["user_info"]["salt"] = salt
    st.session_state["user_info"]["pwd_key"] = new_key
    with open(LOGIN_DB, "r") as json_db:
        info = json.load(json_db)

    info[st.session_state["user"]] = st.session_state["user_info"]

    with open(LOGIN_DB, "w") as json_db:
        json.dump(info, json_db, indent=4)
    return True


def _do_login(user, pwd):
    st.session_state["user"] = user
    st.session_state["login_date"] = datetime.datetime.now().strftime(
        "%a %Y-%m-%d, %H:%M:%S"
    )
    st.session_state["is_authenticated"] = True
    return True


def _do_logout():
    # Remove all relevant fileds of user:  <24-09-21, agomezh> #
    st.session_state["user"] = ""
    st.session_state["login_date"] = None
    st.session_state["is_authenticated"] = False
    return True


def _add_user(user: str, pwd: str, salt: "12345678" * 4):

    with open(LOGIN_DB, "r") as json_db:
        info = json.load(json_db)

    user_info = {"user": user, "pwd_key": _pwd2key(pwd, salt), "salt": salt}
    info[user] = user_info

    with open(LOGIN_DB, "w") as json_db:
        json.dump(info, json_db, indent=4)
