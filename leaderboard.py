import streamlit as st
import pandas as pd
from database import get_connection
from credits import total_student_credits


def leaderboard_page():
    st.title("🏆 Global Leaderboard")
    st.caption("Rankings based on total EcoCredits earned.")

    conn = get_connection()
    c = conn.cursor()

    students = c.execute(
        "SELECT id, username FROM users WHERE role='student'"
    ).fetchall()

    board = []
    for sid, username in students:
        student_subjects = c.execute(
            "SELECT subject, grade FROM subjects WHERE user_id=?", (sid,)
        ).fetchall()
        student_achievements = c.execute(
            "SELECT level FROM achievements WHERE user_id=? AND approved=1", (sid,)
        ).fetchall()
        total = total_student_credits(student_subjects, student_achievements)
        board.append([username, total])

    conn.close()

    board.sort(key=lambda x: x[1], reverse=True)

    if not board:
        st.info("No students yet.")
        return

    # Add rank + medal
    rows = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (name, credits) in enumerate(board):
        medal = medals[i] if i < 3 else f"#{i+1}"
        rows.append([medal, name, credits])

    df = pd.DataFrame(rows, columns=["Rank", "Student", "Credits"])
    st.dataframe(df, use_container_width=True, hide_index=True)