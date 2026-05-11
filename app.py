import streamlit as st
from database import setup_database
from auth import login, register
from student import student_panel
from teacher import teacher_panel
from admin import admin_panel
from leaderboard import leaderboard_page
from style import css

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoCredits AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DATABASE SETUP ────────────────────────────────────────────────────────────
setup_database()

# ── LOAD CSS ──────────────────────────────────────────────────────────────────
st.markdown(css, unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = None

# ── LOGIN SCREEN ──────────────────────────────────────────────────────────────
if st.session_state.user is None:

    _, col, _ = st.columns([1, 1.1, 1])

    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align:center;margin-bottom:2rem;">
                <div style="font-family:JetBrains Mono,monospace;
                            font-size:0.6rem;
                            letter-spacing:0.25em;
                            text-transform:uppercase;
                            color:#1e3a4a;
                            margin-bottom:12px;">
                    ◈ INITIALISING SYSTEM
                </div>

                <h1 style="font-family:Orbitron,monospace;
                           font-size:2.2rem;
                           font-weight:900;
                           color:#00d4ff;
                           letter-spacing:0.08em;
                           text-shadow:0 0 30px rgba(0,212,255,0.6),
                                       0 0 80px rgba(0,212,255,0.2);
                           margin:0;">
                    ECOCREDITS
                </h1>

                <div style="font-family:JetBrains Mono,monospace;
                            font-size:0.7rem;
                            letter-spacing:0.15em;
                            text-transform:uppercase;
                            color:#5a8fa8;
                            margin-top:8px;">
                    AI · Academic Achievement System
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="background:linear-gradient(135deg,#0a1628,#0f2040);
                        border:1px solid rgba(0,212,255,0.2);
                        border-radius:20px;
                        padding:2rem;
                        box-shadow:
                            0 0 40px rgba(0,212,255,0.08),
                            inset 0 1px 0 rgba(0,212,255,0.1);">
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_register = st.tabs(["Sign In", "Register"])

        # ── LOGIN TAB ─────────────────────────────────────────────────────────
        with tab_login:

            username = st.text_input(
                "Username",
                key="login_user",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_pw",
                placeholder="Enter password"
            )

            if st.button(
                "Sign In",
                type="primary",
                use_container_width=True
            ):

                if not username or not password:
                    st.error("Please fill in both fields.")

                else:
                    user = login(username, password)

                    if user:
                        st.session_state.user = user
                        st.rerun()

                    else:
                        st.error("Invalid credentials.")

        # ── REGISTER TAB ─────────────────────────────────────────────────────
        with tab_register:

            reg_user = st.text_input(
                "Choose username",
                key="reg_user",
                placeholder="Username"
            )

            reg_pw = st.text_input(
                "Choose password",
                type="password",
                key="reg_pw",
                placeholder="Min 4 characters"
            )

            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True
            ):

                if not reg_user or not reg_pw:
                    st.error("Please fill in both fields.")

                elif len(reg_pw) < 4:
                    st.error("Password must be at least 4 characters.")

                elif register(reg_user, reg_pw):
                    st.success("Account created! Sign in now.")

                else:
                    st.error("Username already taken.")

        st.markdown("</div>", unsafe_allow_html=True)

# ── MAIN APP ──────────────────────────────────────────────────────────────────
else:

    user = st.session_state.user
    role = user[3]

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:

        st.markdown(
            f"""
            <div style="padding:0.5rem 0 1rem;">

                <div style="font-family:JetBrains Mono,monospace;
                            font-size:0.58rem;
                            letter-spacing:0.2em;
                            text-transform:uppercase;
                            color:#1e3a4a;
                            margin-bottom:6px;">
                    ◈ AUTHENTICATED
                </div>

                <div style="font-family:Orbitron,monospace;
                            font-size:1rem;
                            font-weight:700;
                            color:#e8f4f8;
                            letter-spacing:0.04em;">
                    {user[1]}
                </div>

                <div style="font-family:JetBrains Mono,monospace;
                            font-size:0.7rem;
                            color:#00d4ff;
                            margin-top:3px;
                            letter-spacing:0.08em;">
                    {role.upper()}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page = "leaderboard"

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = None

        st.markdown("---")

        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = None
            st.rerun()

    # ── PAGE ROUTING ─────────────────────────────────────────────────────────
    page = st.session_state.get("page")

    if page == "leaderboard":
        leaderboard_page()

    elif role == "student":
        student_panel(user)

    elif role == "teacher":
        teacher_panel(user)

    elif role == "admin":
        admin_panel()