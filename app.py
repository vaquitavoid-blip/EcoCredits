import streamlit as st
from database import setup_database
from auth import login, register
from student import student_panel
from teacher import teacher_panel
from admin import admin_panel
from leaderboard import leaderboard_page
from style import css

setup_database()
st.set_page_config(
    page_title="EcoCredits AI",
    page_icon="🌱",
    layout="wide"
)
st.markdown(css, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = None

# ── Login / Register ──────────────────────────────────────────────────────────
if st.session_state.user is None:

    col_left, col_mid, col_right = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🌱 EcoCredits AI")
        st.caption("Track your academic achievements and earn credits")
        st.markdown("---")

        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pw")
            if st.button("Login", type="primary", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in both fields.")
                else:
                    user = login(username, password)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with tab_register:
            reg_user = st.text_input("Choose a username", key="reg_user")
            reg_pw = st.text_input("Choose a password", type="password", key="reg_pw")
            if st.button("Create Account", type="primary", use_container_width=True):
                if not reg_user or not reg_pw:
                    st.error("Please fill in both fields.")
                elif len(reg_pw) < 4:
                    st.error("Password must be at least 4 characters.")
                elif register(reg_user, reg_pw):
                    st.success("Account created! Please log in.")
                else:
                    st.error("Username already taken.")

# ── Main App ──────────────────────────────────────────────────────────────────
else:
    user = st.session_state.user
    role = user[3]

    with st.sidebar:
        st.markdown(f"### 👤 {user[1]}")
        st.caption(f"Role: **{role}**")
        st.markdown("---")

        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page = "leaderboard"

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = None

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = None
            st.rerun()

    page = st.session_state.get("page")

    if page == "leaderboard":
        leaderboard_page()
    elif role == "student":
        student_panel(user)
    elif role == "teacher":
        teacher_panel(user)
    elif role == "admin":
        admin_panel()