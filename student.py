import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

from database import (
    get_connection, write_audit,
    get_upload_count, increment_upload_count,
    TEACHER_DISPLAY
)
from config import levels, MAX_UPLOADS_PER_DAY, AUTO_APPROVE_LIMIT, subjects as SUBJECT_WEIGHTS
from ai_engine import (
    extract_text, detect_grades, detect_category,
    analyze_achievement_google, should_auto_approve,
    assign_teacher, get_image_hash, extract_best_title,
    extract_all_lines, ALL_SUBJECTS
)
from credits import total_student_credits

GRADE_OPTIONS = ["A*", "A", "B", "C", "D"]
LEVEL_OPTIONS = ["School", "District", "State", "National", "International"]


def student_panel(user):
    user_id  = user[0]
    username = user[1]
    conn     = get_connection()
    c        = conn.cursor()

    try:
        page = st.sidebar.radio(
            "NAVIGATION",
            ["🏠  Dashboard", "📄  Report Card", "🏆  Achievement"]
        )

        subject_data = c.execute(
            "SELECT subject, grade FROM subjects WHERE user_id=?", (user_id,)
        ).fetchall()

        achievement_data = c.execute(
            "SELECT level FROM achievements WHERE user_id=? AND approved=1", (user_id,)
        ).fetchall()

        total_credits = total_student_credits(subject_data, achievement_data)

        auto_row     = c.execute(
            "SELECT auto_approvals, batch_locked FROM users WHERE id=?", (user_id,)
        ).fetchone()
        auto_count   = auto_row[0] if auto_row else 0
        batch_locked = auto_row[1] if auto_row else 0
        remaining    = AUTO_APPROVE_LIMIT - (auto_count % AUTO_APPROVE_LIMIT)
        uploads_today = get_upload_count(user_id)

        st.sidebar.markdown("---")
        st.sidebar.metric("🌱 EcoCredits",          total_credits)
        st.sidebar.metric("⚡ Auto-approvals left",  remaining)
        st.sidebar.metric("📤 Uploads left today",   max(0, MAX_UPLOADS_PER_DAY - uploads_today))
        st.sidebar.markdown("---")

        if batch_locked:
            st.error(
                "🔒 **Batch lock active.** Your teacher must approve your last "
                f"{AUTO_APPROVE_LIMIT} achievements before you can submit more."
            )
            return

        # ══════════════════════════════════════════════
        # DASHBOARD
        # ══════════════════════════════════════════════
        if page == "🏠  Dashboard":
            st.markdown(
                "<h1 style='font-family:Orbitron,monospace;font-size:1.6rem;"
                "font-weight:800;background:linear-gradient(135deg,#34d399,#f59e0b);"
                "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
                "background-clip:text;'>🌱 STUDENT DASHBOARD</h1>",
                unsafe_allow_html=True
            )
            st.caption(f"SESSION · {username.upper()} · {datetime.now().strftime('%d %b %Y %H:%M')}")
            st.markdown("---")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Credits",  total_credits)
            c2.metric("Subjects",       len(subject_data))
            c3.metric("Achievements",   len(achievement_data))
            c4.metric("Uploads Today",  uploads_today)

            st.markdown("---")
            st.subheader("📚 My Subjects")
            if subject_data:
                st.dataframe(
                    pd.DataFrame(subject_data, columns=["Subject", "Grade"]),
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("No subjects yet — upload your report card.")

            st.subheader("🏆 My Achievements")
            achs = c.execute(
                "SELECT title, level, category, approved FROM achievements WHERE user_id=?",
                (user_id,)
            ).fetchall()
            if achs:
                df = pd.DataFrame(achs, columns=["Title", "Level", "Category", "Status"])
                df["Status"] = df["Status"].replace({0: "⏳ Pending", 1: "✅ Approved"})
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No achievements yet.")

        # ══════════════════════════════════════════════
        # REPORT CARD
        # ══════════════════════════════════════════════
        elif page == "📄  Report Card":
            st.markdown(
                "<h1 style='font-family:Orbitron,monospace;font-size:1.6rem;"
                "font-weight:800;background:linear-gradient(135deg,#34d399,#f59e0b);"
                "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
                "background-clip:text;'>📄 REPORT CARD</h1>",
                unsafe_allow_html=True
            )
            st.caption(
                "Upload your report card. AI extracts grades — you can edit them. "
                "Grades go to your class teacher for approval."
            )
            st.markdown("---")

            if uploads_today >= MAX_UPLOADS_PER_DAY:
                st.error(f"🚫 Daily limit reached ({MAX_UPLOADS_PER_DAY}/day). Try tomorrow.")
                return

            uploaded = st.file_uploader(
                "Drop your report card image here",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:
                st.image(uploaded, caption="Uploaded image", width=500)

                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", uploaded.name)
                with open(path, "wb") as f:
                    f.write(uploaded.getbuffer())

                with st.spinner("🔬 Running multi-mode OCR (6 variants × 6 PSM configs)..."):
                    text      = extract_text(path)
                    detected  = detect_grades(text)
                    all_lines = extract_all_lines(path)

                with st.expander("📋 Raw OCR output", expanded=False):
                    st.code(text[:3000], language=None)

                st.markdown("---")
                st.subheader("🎯 Edit & Confirm Grades")
                st.info(
                    "AI detected the grades below. "
                    "**You can edit any subject or grade, add missing ones, or remove incorrect ones.** "
                    "All changes are sent to your class teacher for final approval."
                )

                # Build editable grade table in session state
                if "rc_grades" not in st.session_state or st.session_state.get("rc_fresh"):
                    st.session_state.rc_grades = dict(detected)
                    st.session_state.rc_fresh  = False

                grades_state = st.session_state.rc_grades

                # Show detected grades as editable rows
                st.markdown("**Detected grades (edit if wrong):**")

                to_delete = []
                for subj, grade in list(grades_state.items()):
                    col_s, col_g, col_d = st.columns([3, 2, 1])
                    with col_s:
                        new_subj = st.selectbox(
                            "Subject", ALL_SUBJECTS,
                            index=ALL_SUBJECTS.index(subj) if subj in ALL_SUBJECTS else 0,
                            key=f"rc_subj_{subj}"
                        )
                    with col_g:
                        new_grade = st.selectbox(
                            "Grade", GRADE_OPTIONS,
                            index=GRADE_OPTIONS.index(grade) if grade in GRADE_OPTIONS else 0,
                            key=f"rc_grade_{subj}"
                        )
                    with col_d:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("🗑", key=f"rc_del_{subj}", help="Remove this subject"):
                            to_delete.append(subj)

                    if new_subj != subj:
                        grades_state[new_subj] = grades_state.pop(subj)
                    else:
                        grades_state[subj] = new_grade

                for d in to_delete:
                    grades_state.pop(d, None)

                st.markdown("---")
                st.markdown("**Add a missing subject:**")
                col_add_s, col_add_g, col_add_btn = st.columns([3, 2, 1])
                with col_add_s:
                    add_subj = st.selectbox("Subject to add", ALL_SUBJECTS, key="rc_add_subj")
                with col_add_g:
                    add_grade = st.selectbox("Grade", GRADE_OPTIONS, key="rc_add_grade")
                with col_add_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("➕ Add", key="rc_add_btn"):
                        st.session_state.rc_grades[add_subj] = add_grade
                        st.rerun()

                st.markdown("---")

                # OCR lines for manual reference
                with st.expander("🔍 All OCR lines (for reference)", expanded=False):
                    st.caption("These are every line the AI read. Use them to check for missed subjects.")
                    for line in all_lines[:60]:
                        st.text(line)

                if grades_state:
                    preview_df = pd.DataFrame(
                        grades_state.items(), columns=["Subject", "Grade"]
                    )
                    st.subheader("📋 Final Grade List to Submit")
                    st.dataframe(preview_df, use_container_width=True, hide_index=True)

                    if st.button("📤 Submit for Teacher Approval", type="primary"):
                        existing = c.execute(
                            "SELECT id FROM report_card_queue WHERE user_id=? AND status='pending'",
                            (user_id,)
                        ).fetchone()
                        if existing:
                            st.warning(
                                "⚠️ You already have a report card pending approval. "
                                "Wait for your teacher to review it first."
                            )
                        else:
                            c.execute(
                                """INSERT INTO report_card_queue
                                   (user_id,image_path,detected_json,status,assigned_teacher,submitted_at)
                                   VALUES(?,?,?,?,?,?)""",
                                (
                                    user_id, path, json.dumps(grades_state),
                                    "pending", "class_teacher",
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                )
                            )
                            conn.commit()
                            increment_upload_count(user_id)
                            write_audit(username, "REPORT_CARD_SUBMIT", f"{len(grades_state)} subjects")
                            st.session_state.rc_fresh = True
                            st.success("✅ Sent to Class Teacher for approval!")
                            st.rerun()
                else:
                    st.warning("No grades in the list. Add at least one subject before submitting.")

        # ══════════════════════════════════════════════
        # ACHIEVEMENT
        # ══════════════════════════════════════════════
        elif page == "🏆  Achievement":
            st.markdown(
                "<h1 style='font-family:Orbitron,monospace;font-size:1.6rem;"
                "font-weight:800;background:linear-gradient(135deg,#34d399,#f59e0b);"
                "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
                "background-clip:text;'>🏆 ACHIEVEMENT</h1>",
                unsafe_allow_html=True
            )
            st.caption(
                "Upload your certificate. AI reads it, searches Google + Bing + DuckDuckGo "
                "to verify and classify the level. You can edit everything before submitting."
            )
            st.markdown("---")

            if uploads_today >= MAX_UPLOADS_PER_DAY:
                st.error(f"🚫 Daily limit reached ({MAX_UPLOADS_PER_DAY}/day). Try tomorrow.")
                return

            uploaded = st.file_uploader(
                "Drop your certificate here",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:
                st.image(uploaded, width=420)

                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", uploaded.name)
                with open(path, "wb") as f:
                    f.write(uploaded.getbuffer())

                # Duplicate check
                img_hash  = get_image_hash(path)
                duplicate = c.execute(
                    "SELECT id FROM achievements WHERE user_id=? AND image_hash=?",
                    (user_id, img_hash)
                ).fetchone()
                if duplicate:
                    st.error("🚫 **Duplicate detected.** You have already submitted this certificate.")
                    return

                with st.spinner("🔬 Reading certificate with multi-mode OCR..."):
                    text     = extract_text(path)
                    ai_title = extract_best_title(text)
                    category = detect_category(text)

                with st.expander("📋 Raw OCR output", expanded=False):
                    st.code(text[:2000], language=None)

                st.markdown("---")
                st.subheader("✏️ Edit Achievement Details")
                st.info(
                    "AI pre-filled the fields below from your certificate. "
                    "**Edit any field if incorrect.** "
                    "Editing the title sends it to a teacher for manual review."
                )

                # Editable title
                edited_title = st.text_input(
                    "Achievement / Award Name",
                    value=ai_title,
                    key="ach_title"
                )
                student_edited_title = (
                    edited_title.strip().lower() != ai_title.strip().lower()
                    and edited_title.strip() != ""
                )
                if student_edited_title:
                    st.warning("⚠️ Title edited — will go to teacher for manual verification.")

                # Editable category
                cat_options  = ["Creative Arts","Technology","Science","Finance","Mathematics","Sports","Other"]
                cat_idx      = cat_options.index(category) if category in cat_options else 0
                edited_cat   = st.selectbox("Category", cat_options, index=cat_idx, key="ach_cat")

                final_title = edited_title.strip() or ai_title

                st.markdown("---")

                if st.button("🔍 Verify on Web", type="primary", key="analyse_btn"):
                    st.session_state.update({
                        "ach_analysed":    True,
                        "ach_title_final": final_title,
                        "ach_edited":      student_edited_title,
                        "ach_ocr_text":    text,
                        "ach_category":    edited_cat,
                        "ach_path":        path,
                        "ach_hash":        img_hash,
                    })

                if st.session_state.get("ach_analysed"):
                    final_title    = st.session_state["ach_title_final"]
                    student_edited = st.session_state["ach_edited"]
                    text           = st.session_state["ach_ocr_text"]
                    category       = st.session_state["ach_category"]
                    img_hash       = st.session_state["ach_hash"]
                    path           = st.session_state["ach_path"]

                    with st.spinner("🌐 Searching Google + Bing + DuckDuckGo..."):
                        result = analyze_achievement_google(final_title)

                    with st.expander("📋 Web verification log", expanded=True):
                        for line in result["log"]:
                            st.markdown(line)

                    st.markdown("---")
                    st.subheader("🤖 AI Results")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Category",      category)
                    col2.metric("Detected Level", result["level"])
                    col3.metric("Confidence",     result["confidence"])

                    # Editable level override
                    level = st.selectbox(
                        "Confirm / Override Level",
                        LEVEL_OPTIONS,
                        index=LEVEL_OPTIONS.index(result["level"]),
                        key="ach_level_select"
                    )

                    # Approval logic
                    auto_row2     = c.execute(
                        "SELECT auto_approvals FROM users WHERE id=?", (user_id,)
                    ).fetchone()
                    cur_auto      = auto_row2[0] if auto_row2 else 0
                    force_teacher = cur_auto > 0 and cur_auto % AUTO_APPROVE_LIMIT == 0
                    raw_auto      = should_auto_approve(result["confidence"], result["is_irrational"])
                    teacher       = assign_teacher(category)
                    auto_approve  = 0

                    st.markdown("---")
                    if student_edited:
                        st.error("👨‍🏫 Title was edited — going to teacher for verification.")
                    elif force_teacher:
                        st.warning(f"⚠️ {AUTO_APPROVE_LIMIT} auto-approvals reached — routine teacher check.")
                    elif result["is_irrational"]:
                        st.error("🚨 Could not verify online — going to teacher.")
                    elif raw_auto:
                        st.success("✅ Verified — will be auto-approved.")
                        auto_approve = 1
                    else:
                        st.warning("⚠️ Low confidence — going to teacher.")

                    if auto_approve:
                        st.info("🤖 This will be **auto-approved** immediately.")
                    else:
                        st.info(f"👨‍🏫 Will go to: **{TEACHER_DISPLAY.get(teacher, teacher)}**")

                    st.markdown("---")

                    if st.button("📤 Submit Achievement", type="primary", key="submit_ach"):
                        if not final_title.strip():
                            st.error("Please enter the achievement name.")
                        else:
                            batch_num = (cur_auto // AUTO_APPROVE_LIMIT) + 1
                            c.execute(
                                """INSERT INTO achievements
                                   (user_id,title,level,category,approved,
                                    assigned_teacher,batch_number,image_hash,submitted_date)
                                   VALUES(?,?,?,?,?,?,?,?,?)""",
                                (
                                    user_id, final_title, level, category,
                                    auto_approve, teacher, batch_num, img_hash,
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                )
                            )
                            ach_id = c.lastrowid

                            if auto_approve == 0:
                                c.execute(
                                    "INSERT INTO approval_queue(achievement_id,status) VALUES(?,?)",
                                    (ach_id, "pending")
                                )
                            else:
                                new_count = cur_auto + 1
                                c.execute(
                                    "UPDATE users SET auto_approvals=? WHERE id=?",
                                    (new_count, user_id)
                                )
                                if new_count % AUTO_APPROVE_LIMIT == 0:
                                    c.execute(
                                        "UPDATE users SET batch_locked=1 WHERE id=?", (user_id,)
                                    )

                            increment_upload_count(user_id)
                            conn.commit()
                            write_audit(
                                username, "ACHIEVEMENT_SUBMIT",
                                f"{final_title} | {level} | auto:{auto_approve}"
                            )

                            for k in ["ach_analysed","ach_title_final","ach_edited",
                                      "ach_ocr_text","ach_category","ach_path","ach_hash"]:
                                st.session_state.pop(k, None)

                            st.success("🎉 Auto-approved!" if auto_approve else "📬 Sent to teacher!")
                            st.rerun()

    finally:
        conn.close()