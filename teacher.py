import streamlit as st
import pandas as pd
import json
import os

from database import get_connection


def teacher_panel(user):

    username = user[1]

    st.title("🧑‍🏫 Teacher Panel")

    conn = get_connection()

    c = conn.cursor()

    # =========================================================
    # REPORT CARD APPROVALS
    # =========================================================

    st.header("📄 Pending Report Cards")

    report_cards = c.execute(
        """
        SELECT
            id,
            user_id,
            image_path,
            detected_json,
            status

        FROM report_card_queue

        WHERE assigned_teacher=?
        AND status='pending'
        """,
        (username,)
    ).fetchall()

    if not report_cards:

        st.info("No pending report cards.")

    else:

        for report in report_cards:

            queue_id = report[0]

            student_id = report[1]

            image_path = report[2]

            detected_json = report[3]

            student = c.execute(
                """
                SELECT username
                FROM users
                WHERE id=?
                """,
                (student_id,)
            ).fetchone()

            student_name = (
                student[0]
                if student
                else "Unknown"
            )

            st.markdown("---")

            st.subheader(
                f"👤 {student_name}"
            )

            # IMAGE
            if image_path and os.path.exists(image_path):

                st.image(
                    image_path,
                    width=600
                )

            else:

                st.warning(
                    "Image not found."
                )

            # GRADES
            try:

                grades = json.loads(
                    detected_json
                )

            except:

                grades = {}

            if grades:

                df = pd.DataFrame(
                    list(grades.items()),
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

                st.warning(
                    "No grades detected."
                )

            col1, col2 = st.columns(2)

            # APPROVE
            with col1:

                if st.button(
                    f"✅ Approve Report Card {queue_id}",
                    key=f"approve_{queue_id}"
                ):

                    # delete old subjects
                    c.execute(
                        """
                        DELETE FROM subjects
                        WHERE user_id=?
                        """,
                        (student_id,)
                    )

                    # insert approved grades
                    for subject, grade in grades.items():

                        c.execute(
                            """
                            INSERT INTO subjects(
                                user_id,
                                subject,
                                grade,
                                approved
                            )
                            VALUES(?,?,?,?)
                            """,
                            (
                                student_id,
                                subject,
                                grade,
                                1
                            )
                        )

                    # mark queue approved
                    c.execute(
                        """
                        UPDATE report_card_queue
                        SET status='approved'
                        WHERE id=?
                        """,
                        (queue_id,)
                    )

                    conn.commit()

                    st.success(
                        "Report Card Approved"
                    )

                    st.rerun()

            # REJECT
            with col2:

                if st.button(
                    f"❌ Reject Report Card {queue_id}",
                    key=f"reject_{queue_id}"
                ):

                    c.execute(
                        """
                        UPDATE report_card_queue
                        SET status='rejected'
                        WHERE id=?
                        """,
                        (queue_id,)
                    )

                    conn.commit()

                    st.error(
                        "Report Card Rejected"
                    )

                    st.rerun()

    # =========================================================
    # ACHIEVEMENT APPROVALS
    # =========================================================

    st.markdown("---")

    st.header("🏆 Pending Achievements")

    pending = c.execute(
        """
        SELECT
            approval_queue.id,
            achievements.id,
            achievements.title,
            achievements.level,
            achievements.category

        FROM approval_queue

        JOIN achievements
        ON approval_queue.achievement_id
        =
        achievements.id

        WHERE achievements.assigned_teacher=?
        AND approval_queue.status='pending'
        """,
        (username,)
    ).fetchall()

    if not pending:

        st.success(
            "No Pending Achievements"
        )

    for p in pending:

        st.markdown("---")

        st.subheader(p[2])

        st.write(f"🌍 Level: {p[3]}")

        st.write(f"📚 Category: {p[4]}")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"Approve Achievement {p[0]}",
                key=f"ach_approve_{p[0]}"
            ):

                c.execute(
                    """
                    UPDATE achievements
                    SET approved=1
                    WHERE id=?
                    """,
                    (p[1],)
                )

                c.execute(
                    """
                    UPDATE approval_queue
                    SET status='approved'
                    WHERE id=?
                    """,
                    (p[0],)
                )

                conn.commit()

                st.success(
                    "Achievement Approved"
                )

                st.rerun()

        with col2:

            if st.button(
                f"Reject Achievement {p[0]}",
                key=f"ach_reject_{p[0]}"
            ):

                c.execute(
                    """
                    DELETE FROM achievements
                    WHERE id=?
                    """,
                    (p[1],)
                )

                c.execute(
                    """
                    DELETE FROM approval_queue
                    WHERE id=?
                    """,
                    (p[0],)
                )

                conn.commit()

                st.error(
                    "Achievement Rejected"
                )

                st.rerun()

    conn.close()