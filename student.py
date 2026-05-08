import streamlit as st
import pandas as pd
import os
import json

from database import (
    get_connection,
    SUBJECT_TEACHER_MAP
)

from ai_engine import (
    extract_text,
    detect_grades,
    detect_category,
    analyze_achievement_google,
    should_auto_approve,
    assign_teacher
)

from credits import total_student_credits

AUTO_APPROVE_LIMIT = 5


def student_panel(user):

    user_id = user[0]

    conn = get_connection()

    c = conn.cursor()

    try:

        page = st.sidebar.radio(
            "📋 Menu",
            [
                "🏠 Dashboard",
                "📄 Upload Report Card",
                "🏆 Upload Achievement"
            ]
        )

        # ─────────────────────────────────────
        # LOAD DATA
        # ─────────────────────────────────────

        subject_data = c.execute(
            """
            SELECT subject, grade
            FROM subjects
            WHERE user_id=?
            AND approved=1
            """,
            (user_id,)
        ).fetchall()

        achievement_data = c.execute(
            """
            SELECT level
            FROM achievements
            WHERE user_id=?
            AND approved=1
            """,
            (user_id,)
        ).fetchall()

        total_credits = total_student_credits(
            subject_data,
            achievement_data
        )

        st.sidebar.metric(
            "🌱 EcoCredits",
            total_credits
        )

        # ─────────────────────────────────────
        # DASHBOARD
        # ─────────────────────────────────────

        if page == "🏠 Dashboard":

            st.title("🌱 Student Dashboard")

            # SUBJECTS

            st.subheader("📚 Approved Subjects")

            if subject_data:

                df = pd.DataFrame(
                    subject_data,
                    columns=[
                        "Subject",
                        "Grade"
                    ]
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No approved subjects yet."
                )

            # PENDING REPORT CARD

            st.subheader("🕒 Pending Report Cards")

            pending_cards = c.execute(
                """
                SELECT status
                FROM report_card_queue
                WHERE user_id=?
                """,
                (user_id,)
            ).fetchall()

            if pending_cards:

                for p in pending_cards:

                    st.warning(
                        f"Status: {p[0]}"
                    )

            else:

                st.success(
                    "No pending report cards"
                )

            # ACHIEVEMENTS

            st.subheader("🏆 Achievements")

            achievements = c.execute(
                """
                SELECT
                title,
                level,
                category,
                approved
                FROM achievements
                WHERE user_id=?
                """,
                (user_id,)
            ).fetchall()

            if achievements:

                adf = pd.DataFrame(
                    achievements,
                    columns=[
                        "Title",
                        "Level",
                        "Category",
                        "Approved"
                    ]
                )

                st.dataframe(
                    adf,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No achievements uploaded."
                )

        # ─────────────────────────────────────
        # REPORT CARD
        # ─────────────────────────────────────

        elif page == "📄 Upload Report Card":

            st.title("📄 AI Report Card Reader")

            uploaded = st.file_uploader(
                "Upload Report Card",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                path = os.path.join(
                    "uploads",
                    uploaded.name
                )

                with open(path, "wb") as f:

                    f.write(
                        uploaded.getbuffer()
                    )

                with st.spinner(
                    "Reading Report Card..."
                ):

                    text = extract_text(path)

                with st.expander(
                    "OCR TEXT"
                ):

                    st.code(text[:3000])

                detected = detect_grades(text)

                all_subjects = [

                    "Add Maths",
                    "Extended Maths",
                    "FLE",
                    "ESL",
                    "Physics",
                    "Chemistry",
                    "Biology",
                    "Combined Science",
                    "ICT",
                    "Economics",
                    "Business Studies",
                    "Accounting",
                    "DT",
                    "Art and Design"
                ]

                st.markdown(
                    "### ✏️ Edit Grades"
                )

                editable = {}

                for subject in all_subjects:

                    default_grade = detected.get(
                        subject,
                        ""
                    )

                    col1, col2 = st.columns([3, 1])

                    with col1:

                        st.write(subject)

                    with col2:

                        grade = st.selectbox(
                            f"Grade {subject}",
                            ["", "A*", "A", "B", "C", "D"],
                            index=["", "A*", "A", "B", "C", "D"].index(default_grade)
                            if default_grade in ["A*", "A", "B", "C", "D"]
                            else 0,
                            key=subject
                        )

                        if grade != "":

                            editable[subject] = grade

                st.markdown("---")

                if st.button(
                    "📤 Submit To Teacher",
                    type="primary"
                ):

                    if len(editable) == 0:

                        st.error(
                            "Please enter at least one subject."
                        )

                    else:

                        assigned_teacher = "class_teacher"

                        detected_json = json.dumps(
                            editable
                        )

                        c.execute(
                            """
                            INSERT INTO report_card_queue(

                                user_id,
                                image_path,
                                detected_json,
                                status,
                                assigned_teacher

                            )
                            VALUES(?,?,?,?,?)
                            """,
                            (
                                user_id,
                                path,
                                detected_json,
                                "pending",
                                assigned_teacher
                            )
                        )

                        conn.commit()

                        st.success(
                            "✅ Report Card Submitted To Teacher"
                        )

                        st.info(
                            "Waiting for approval."
                        )

                        st.rerun()

        # ─────────────────────────────────────
        # ACHIEVEMENTS
        # ─────────────────────────────────────

        elif page == "🏆 Upload Achievement":

            st.title("🏆 Achievement Upload")

            uploaded = st.file_uploader(
                "Upload Certificate",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                path = os.path.join(
                    "uploads",
                    uploaded.name
                )

                with open(path, "wb") as f:

                    f.write(
                        uploaded.getbuffer()
                    )

                text = extract_text(path)

                st.image(
                    uploaded,
                    width=400
                )

                title = st.text_input(
                    "Achievement Name"
                )

                if title:

                    category = detect_category(
                        text
                    )

                    result = analyze_achievement_google(
                        title
                    )

                    st.subheader(
                        "AI Analysis"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Category",
                        category
                    )

                    col2.metric(
                        "Level",
                        result["level"]
                    )

                    col3.metric(
                        "Confidence",
                        result["confidence"]
                    )

                    auto = should_auto_approve(
                        result["confidence"],
                        result["is_irrational"]
                    )

                    teacher = assign_teacher(
                        category
                    )

                    if auto:

                        st.success(
                            "Auto approval enabled"
                        )

                    else:

                        st.warning(
                            "Teacher approval required"
                        )

                    if st.button(
                        "Submit Achievement",
                        type="primary"
                    ):

                        c.execute(
                            """
                            INSERT INTO achievements(

                                user_id,
                                title,
                                level,
                                category,
                                approved,
                                assigned_teacher

                            )
                            VALUES(?,?,?,?,?,?)
                            """,
                            (
                                user_id,
                                title,
                                result["level"],
                                category,
                                1 if auto else 0,
                                teacher
                            )
                        )

                        achievement_id = c.lastrowid

                        if not auto:

                            c.execute(
                                """
                                INSERT INTO approval_queue(

                                    achievement_id,
                                    status

                                )
                                VALUES(?,?)
                                """,
                                (
                                    achievement_id,
                                    "pending"
                                )
                            )

                        conn.commit()

                        st.success(
                            "Achievement Submitted"
                        )

                        st.rerun()

    finally:

        conn.close()