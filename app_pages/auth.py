import streamlit as st
from services.auth_service import (
    check_login,
    email_already_registered,
    register_user,
    user_file_exists
)


def show_auth():
    st.markdown(
        "<h2 style='text-align: center; color: #004d99;'>🔐 Olympics Analyzer - Login / Register</h2>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            login_email = st.text_input("Email").strip()
            login_password = st.text_input("Password", type="password").strip()
            login_submit = st.form_submit_button("Login")

            if login_submit:
                if not user_file_exists():
                    st.error("🚫 No registered users found. Please register first.")
                else:
                    login_success, user_name = check_login(login_email, login_password)

                    if login_success:
                        st.success(f"✅ Welcome back, {user_name}!")
                        st.session_state["user_logged_in"] = True
                        st.session_state["user_name"] = user_name
                        st.rerun()
                    else:
                        st.error("❌ Incorrect email or password.")

    with tab2:
        with st.form("registration_form"):
            name = st.text_input("Name").strip()
            email = st.text_input("Email").strip()
            password = st.text_input("Password", type="password").strip()
            submit = st.form_submit_button("Register")

            if submit:
                if name == "" or email == "" or password == "":
                    st.warning("⚠️ Please fill in all fields.")
                elif not ("@" in email and "." in email):
                    st.warning("📧 Please enter a valid email address.")
                elif email_already_registered(email):
                    st.warning("⚠️ This email is already registered. Please log in.")
                else:
                    register_user(name, email, password)
                    st.success(f"✅ Welcome, {name}! Registration successful. Please log in.")