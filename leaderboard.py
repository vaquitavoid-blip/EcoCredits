import streamlit as st
import pandas as pd
from database import get_connection
from credits import total_student_credits


def leaderboard_page():
    st.markdown(
        "<h1 style='font-family:Orbitron,monospace;color:#00d4ff;"
        "text-shadow:0 0 20px rgba(0,212,255,0.5);'>🏆 LEADERBOARD</h1>",
        unsafe_allow_html=True
    )
    st.caption("Global rankings based on verified EcoCredits.")
    st.markdown("---")

    conn = get_connection()
    c    = conn.cursor()

    students = c.execute(
        "SELECT id, username FROM users WHERE role='student'"
    ).fetchall()

    board = []
    for sid, username in students:
        s_sub = c.execute(
            "SELECT subject, grade FROM subjects WHERE user_id=?", (sid,)
        ).fetchall()
        s_ach = c.execute(
            "SELECT level FROM achievements WHERE user_id=? AND approved=1", (sid,)
        ).fetchall()
        total = total_student_credits(s_sub, s_ach)
        board.append([username, total, len(s_sub), len(s_ach)])

    conn.close()
    board.sort(key=lambda x: x[1], reverse=True)

    if not board:
        st.info("No students yet.")
        return

    medals = ["🥇", "🥈", "🥉"]
    rows   = []
    for i, (name, credits, nsub, nach) in enumerate(board):
        rank = medals[i] if i < 3 else f"#{i+1}"
        rows.append([rank, name, credits, nsub, nach])

    df = pd.DataFrame(rows, columns=["Rank","Student","Credits","Subjects","Achievements"])
    st.dataframe(df, use_container_width=True, hide_index=True)