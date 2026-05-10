import streamlit as st
import pandas as pd
import json
import os

from database import get_connection, write_audit, TEACHER_DISPLAY


def teacher_panel(user):
    username = user[1]
    conn     = get_connection()
    c        = conn.cursor()

    st.markdown(
        "<h1 style='font-family:Orbitron,monospace;color:#00d4ff;"
        "text-shadow:0 0 20px rgba(0,212,255,0.5);'>🧑‍🏫 TEACHER PANEL</h1>",
        unsafe_allow_html=True
    )
    st.caption(f"Logged in as **{TEACHER_DISPLAY.get(username, username)}**")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📄 Report Cards", "🏆 Achievements"])

    # ── REPORT CARDS ─────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Pending Report Cards")

        report_cards = c.execute(
            """
            SELECT rq.id, rq.user_id, rq.image_path,
                   rq.detected_json, rq.submitted_at, u.username
            FROM report_card_queue rq
            JOIN users u ON rq.user_id = u.id
            WHERE rq.assigned_teacher=? AND rq.status='pending'
            """,
            (username,)
        ).fetchall()

        if not report_cards:
            st.success("✅ No pending report cards.")
        else:
            for rc in report_cards:
                queue_id     = rc[0]
                student_id   = rc[1]
                image_path   = rc[2]
                detected_raw = rc[3]
                submitted_at = rc[4]
                student_name = rc[5]

                st.markdown(f"### 👤 {student_name}")
                st.caption(f"Submitted: {submitted_at}")

                col_img, col_grades = st.columns([1, 1])

                with col_img:
                    if image_path and os.path.exists(image_path):
                        st.image(image_path, use_column_width=True)
                    else:
                        st.warning("Image not found on server.")

                with col_grades:
                    try:
                        grades = json.loads(detected_raw) if detected_raw else {}
                    except Exception:
                        grades = {}

                    if grades:
                        st.dataframe(
                            pd.DataFrame(grades.items(), columns=["Subject", "Grade"]),
                            use_container_width=True, hide_index=True
                        )
                    else:
                        st.warning("No grades detected by AI.")

                    st.markdown("**Override a grade (optional):**")
                    all_subjects = list(grades.keys()) if grades else ["—"]
                    sel_subj = st.selectbox("Subject", all_subjects, key=f"subj_{queue_id}")
                    override_grade = st.selectbox(
                        "Grade", ["—", "A*", "A", "B", "C", "D"],
                        key=f"grade_{queue_id}"
                    )
                    if st.button("✏️ Apply Override", key=f"override_{queue_id}"):
                        if override_grade != "—" and sel_subj in grades:
                            grades[sel_subj] = override_grade
                            c.execute(
                                "UPDATE report_card_queue SET detected_json=? WHERE id=?",
                                (json.dumps(grades), queue_id)
                            )
                            conn.commit()
                            st.success(f"Updated {sel_subj} → {override_grade}")
                            st.rerun()

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve", key=f"rc_approve_{queue_id}", type="primary"):
                        c.execute("DELETE FROM subjects WHERE user_id=?", (student_id,))
                        for subj, grade in grades.items():
                            c.execute(
                                "INSERT INTO subjects(user_id,subject,grade,approved,teacher) VALUES(?,?,?,?,?)",
                                (student_id, subj, grade, 1, username)
                            )
                        c.execute(
                            "UPDATE report_card_queue SET status='approved' WHERE id=?",
                            (queue_id,)
                        )
                        conn.commit()
                        write_audit(username, "REPORT_CARD_APPROVE", f"Student: {student_name}")
                        st.success("✅ Approved and grades saved!")
                        st.rerun()

                with col2:
                    if st.button(f"❌ Reject", key=f"rc_reject_{queue_id}"):
                        c.execute(
                            "UPDATE report_card_queue SET status='rejected' WHERE id=?",
                            (queue_id,)
                        )
                        conn.commit()
                        write_audit(username, "REPORT_CARD_REJECT", f"Student: {student_name}")
                        st.error("Report card rejected.")
                        st.rerun()

                st.markdown("---")

    # ── ACHIEVEMENTS ──────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Pending Achievements")

        pending = c.execute(
            """
            SELECT aq.id, a.id, a.title, a.level,
                   a.category, u.username, u.id
            FROM approval_queue aq
            JOIN achievements a ON aq.achievement_id = a.id
            JOIN users u ON a.user_id = u.id
            WHERE a.assigned_teacher=? AND aq.status='pending'
            ORDER BY aq.id ASC
            """,
            (username,)
        ).fetchall()

        if not pending:
            st.success("✅ No pending achievements.")
        else:
            st.info(
                f"**{len(pending)}** achievement(s) pending review. "
                "Approving all clears the student's batch lock."
            )

            for p in pending:
                queue_id   = p[0]
                ach_id     = p[1]
                title      = p[2]
                level      = p[3]
                category   = p[4]
                sname      = p[5]
                student_id = p[6]

                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.markdown(f"**{title}**")
                    st.caption(f"👤 {sname}  ·  🌍 {level}  ·  📚 {category}")

                with col_actions:
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("✅", key=f"ach_app_{queue_id}", type="primary"):
                            c.execute("UPDATE achievements SET approved=1 WHERE id=?", (ach_id,))
                            c.execute("UPDATE approval_queue SET status='approved' WHERE id=?", (queue_id,))
                            # Unlock batch if all cleared
                            still = c.execute(
                                """SELECT COUNT(*) FROM approval_queue aq
                                   JOIN achievements a ON aq.achievement_id=a.id
                                   WHERE a.user_id=? AND aq.status='pending'""",
                                (student_id,)
                            ).fetchone()[0]
                            if still == 0:
                                c.execute("UPDATE users SET batch_locked=0 WHERE id=?", (student_id,))
                            conn.commit()
                            write_audit(username, "ACHIEVEMENT_APPROVE", title)
                            st.rerun()

                    with b2:
                        if st.button("❌", key=f"ach_rej_{queue_id}"):
                            c.execute("DELETE FROM achievements WHERE id=?", (ach_id,))
                            c.execute("DELETE FROM approval_queue WHERE id=?", (queue_id,))
                            still = c.execute(
                                """SELECT COUNT(*) FROM approval_queue aq
                                   JOIN achievements a ON aq.achievement_id=a.id
                                   WHERE a.user_id=? AND aq.status='pending'""",
                                (student_id,)
                            ).fetchone()[0]
                            if still == 0:
                                c.execute("UPDATE users SET batch_locked=0 WHERE id=?", (student_id,))
                            conn.commit()
                            write_audit(username, "ACHIEVEMENT_REJECT", title)
                            st.rerun()

                st.markdown("---")

    conn.close()