import streamlit as st
import pandas as pd
import os

from database import get_connection
from config import levels
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


# ─────────────────────────────────────────────
# TITLE EXTRACTION
# Tries to find the most likely award title
# from OCR text using multiple strategies
# ─────────────────────────────────────────────

def extract_best_title(text):
    """
    Tries multiple strategies to find the certificate title.
    Returns the best candidate string.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Strategy 1: Look for lines with known title keywords
    title_keywords = [
        "certificate", "award", "competition", "olympiad",
        "achievement", "recognition", "excellence", "merit",
        "winner", "champion", "participation", "prize"
    ]

    keyword_lines = []
    for line in lines:
        lower = line.lower()
        if any(kw in lower for kw in title_keywords):
            # Prefer longer lines with keywords (more descriptive)
            keyword_lines.append((len(line), line))

    if keyword_lines:
        keyword_lines.sort(reverse=True)
        return keyword_lines[0][1]

    # Strategy 2: Look for lines that are ALL CAPS (usually the title)
    caps_lines = [l for l in lines if l.isupper() and len(l) > 5]
    if caps_lines:
        return max(caps_lines, key=len)

    # Strategy 3: Take the longest line in the top 10 lines
    top_lines = lines[:10]
    if top_lines:
        return max(top_lines, key=len)

    # Strategy 4: Just return first non-empty line
    return lines[0] if lines else ""


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

        subject_data = c.execute(
            "SELECT subject, grade FROM subjects WHERE user_id=?",
            (user_id,)
        ).fetchall()

        achievement_data = c.execute(
            "SELECT level FROM achievements WHERE user_id=? AND approved=1",
            (user_id,)
        ).fetchall()

        total_credits = total_student_credits(
            subject_data,
            achievement_data
        )

        # Sidebar stats
        st.sidebar.markdown("---")
        st.sidebar.metric("🌱 EcoCredits", total_credits)

        auto_count_row = c.execute(
            "SELECT auto_approvals FROM users WHERE id=?",
            (user_id,)
        ).fetchone()

        auto_count = auto_count_row[0] if auto_count_row else 0
        remaining = AUTO_APPROVE_LIMIT - (auto_count % AUTO_APPROVE_LIMIT)

        st.sidebar.metric(
            "🤖 Auto-approvals before check",
            remaining
        )

        st.sidebar.markdown("---")

        # ─────────────────────────────────────────────
        # DASHBOARD
        # ─────────────────────────────────────────────

        if page == "🏠 Dashboard":

            st.title("🌱 Student Dashboard")
            st.caption(f"Welcome back, **{user[1]}**")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Credits", total_credits)
            col2.metric("Subjects", len(subject_data))
            col3.metric("Achievements", len(achievement_data))

            st.markdown("---")

            st.subheader("📚 My Subjects")

            if subject_data:
                st.dataframe(
                    pd.DataFrame(
                        subject_data,
                        columns=["Subject", "Grade"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No subjects yet — upload your report card.")

            st.subheader("🏆 My Achievements")

            achievements = c.execute(
                """
                SELECT title, level, category, approved
                FROM achievements
                WHERE user_id=?
                """,
                (user_id,)
            ).fetchall()

            if achievements:
                ach_df = pd.DataFrame(
                    achievements,
                    columns=["Title", "Level", "Category", "Status"]
                )
                ach_df["Status"] = ach_df["Status"].replace(
                    {0: "⏳ Pending", 1: "✅ Approved"}
                )
                st.dataframe(
                    ach_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No achievements yet — upload a certificate.")

        # ─────────────────────────────────────────────
        # REPORT CARD
        # ─────────────────────────────────────────────

        elif page == "📄 Upload Report Card":

            st.title("📄 AI Report Card Reader")
            st.caption(
                "Upload a clear image of your report card. "
                "AI will extract grades automatically."
            )

            uploaded = st.file_uploader(
                "Choose report card image",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:

                col_img, col_info = st.columns([1, 1])

                with col_img:
                    st.image(
                        uploaded,
                        caption="Uploaded image",
                        use_column_width=True
                    )

                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", uploaded.name)

                with open(path, "wb") as f:
                    f.write(uploaded.getbuffer())

                with st.spinner("🔍 Running OCR..."):
                    text = extract_text(path)

                with st.expander("🔎 Raw OCR text (click to expand)"):
                    st.code(text[:3000])

                with st.spinner("🧠 Detecting grades..."):
                    detected = detect_grades(text)

                st.markdown("---")
                st.subheader("🎯 Detected Grades")

                if detected:
                    det_df = pd.DataFrame(
                        detected.items(),
                        columns=["Subject", "Grade"]
                    )
                    st.dataframe(
                        det_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(
                        f"Found **{len(detected)}** subject(s) successfully."
                    )

                    if st.button("💾 Save These Grades", type="primary"):
                        c.execute(
                            "DELETE FROM subjects WHERE user_id=?",
                            (user_id,)
                        )
                        for subject, grade in detected.items():
                            c.execute(
                                """
                                INSERT INTO subjects(
                                    user_id, subject, grade, approved
                                )
                                VALUES(?,?,?,?)
                                """,
                                (user_id, subject, grade, 1)
                            )
                        conn.commit()
                        st.success("✅ Grades saved!")
                        st.rerun()

                else:
                    st.warning(
                        "⚠️ No grades detected. Tips:\n"
                        "- Use a clearer, higher resolution image\n"
                        "- Make sure subject names are visible\n"
                        "- Avoid shadows or glare"
                    )

        # ─────────────────────────────────────────────
        # ACHIEVEMENT UPLOAD
        # ─────────────────────────────────────────────

        elif page == "🏆 Upload Achievement":

            st.title("🏆 Achievement Upload")
            st.caption(
                "Upload your certificate. "
                "AI reads it, searches the web to verify, "
                "then classifies the level."
            )

            uploaded = st.file_uploader(
                "Choose certificate image",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:

                st.image(
                    uploaded,
                    caption="Uploaded certificate",
                    use_column_width=False,
                    width=420
                )

                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", uploaded.name)

                with open(path, "wb") as f:
                    f.write(uploaded.getbuffer())

                # ── OCR ──────────────────────────────
                with st.spinner("🔍 Reading certificate..."):
                    text = extract_text(path)

                with st.expander("🔎 Raw OCR text"):
                    st.code(text[:2000])

                # ── AI title extraction ───────────────
                ai_title = extract_best_title(text)

                st.markdown("---")
                st.subheader("✏️ Confirm Achievement Name")

                st.info(
                    f"🤖 AI read the title as: **{ai_title}**\n\n"
                    "If this is correct, leave it as-is and click Analyse. "
                    "If you edit it, your submission will go to a teacher for manual review."
                )

                # Track if student edits the title
                edited_title = st.text_input(
                    "Achievement / Award Name",
                    value=ai_title,
                    key="title_input"
                )

                student_edited = (
                    edited_title.strip().lower() != ai_title.strip().lower()
                    and edited_title.strip() != ""
                )

                if student_edited:
                    st.warning(
                        "⚠️ You edited the title — "
                        "this submission will go to a teacher for verification."
                    )

                final_title = edited_title.strip() if edited_title.strip() else ai_title

                # ── Analyse button ────────────────────
                if st.button("🔍 Analyse Achievement", type="primary"):
                    st.session_state["analysed"] = True
                    st.session_state["final_title"] = final_title
                    st.session_state["student_edited"] = student_edited
                    st.session_state["ocr_text"] = text

                if st.session_state.get("analysed"):

                    final_title    = st.session_state["final_title"]
                    student_edited = st.session_state["student_edited"]
                    text           = st.session_state["ocr_text"]

                    category = detect_category(text)

                    with st.spinner(
                        "🌐 Searching web to verify achievement..."
                    ):
                        result = analyze_achievement_google(final_title)

                    # ── Google log ────────────────────
                    with st.expander(
                        "📋 Google verification log",
                        expanded=True
                    ):
                        for line in result["log"]:
                            st.markdown(line)

                    st.markdown("---")
                    st.subheader("🤖 AI Analysis")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Category",       category)
                    col2.metric("Detected Level",  result["level"])
                    col3.metric("Confidence",      result["confidence"])

                    # ── Approval logic ────────────────
                    auto_count_row = c.execute(
                        "SELECT auto_approvals FROM users WHERE id=?",
                        (user_id,)
                    ).fetchone()

                    current_count = auto_count_row[0] if auto_count_row else 0
                    force_teacher = (
                        current_count > 0
                        and current_count % AUTO_APPROVE_LIMIT == 0
                    )

                    raw_auto = should_auto_approve(
                        result["confidence"],
                        result["is_irrational"]
                    )

                    # Force to teacher if:
                    # 1. Student edited the title
                    # 2. Hit the 5-approval batch limit
                    # 3. AI is not confident
                    if student_edited:
                        auto_approve = 0
                        st.error(
                            "👨‍🏫 Sending to teacher — "
                            "title was manually edited."
                        )

                    elif force_teacher:
                        auto_approve = 0
                        st.warning(
                            f"⚠️ {AUTO_APPROVE_LIMIT} auto-approvals reached — "
                            "routine teacher check required."
                        )

                    elif result["is_irrational"]:
                        auto_approve = 0
                        st.error(
                            "🚨 Could not verify on Google — "
                            "sending to teacher."
                        )

                    elif raw_auto:
                        auto_approve = 1
                        st.success(
                            "✅ Verified — will be auto-approved."
                        )

                    else:
                        auto_approve = 0
                        st.warning(
                            "⚠️ Low confidence — sending to teacher."
                        )

                    teacher = assign_teacher(category)

                    # ── Level override ────────────────
                    level_options = [
                        "School",
                        "District",
                        "State",
                        "National",
                        "International"
                    ]

                    level = st.selectbox(
                        "Confirm / Override Level",
                        level_options,
                        index=level_options.index(result["level"])
                    )

                    st.markdown("---")

                    if auto_approve:
                        st.info("🤖 This will be **auto-approved**.")
                    else:
                        st.info(
                            f"👨‍🏫 This will go to **{teacher}** for approval."
                        )

                    # ── Submit ────────────────────────
                    if st.button("📤 Submit Achievement", type="primary"):

                        if not final_title:
                            st.error("Please enter the achievement name.")

                        else:

                            c.execute(
                                """
                                INSERT INTO achievements(
                                    user_id, title, level,
                                    category, approved, assigned_teacher
                                )
                                VALUES(?,?,?,?,?,?)
                                """,
                                (
                                    user_id,
                                    final_title,
                                    level,
                                    category,
                                    auto_approve,
                                    teacher
                                )
                            )

                            achievement_id = c.lastrowid

                            if auto_approve == 0:
                                c.execute(
                                    """
                                    INSERT INTO approval_queue(
                                        achievement_id, status
                                    )
                                    VALUES(?,?)
                                    """,
                                    (achievement_id, "pending")
                                )
                            else:
                                # Increment auto-approval counter
                                c.execute(
                                    """
                                    UPDATE users
                                    SET auto_approvals = auto_approvals + 1
                                    WHERE id=?
                                    """,
                                    (user_id,)
                                )

                            conn.commit()

                            # Clear session state
                            st.session_state["analysed"]      = False
                            st.session_state["final_title"]   = ""
                            st.session_state["student_edited"] = False

                            if auto_approve:
                                st.success(
                                    "🎉 Achievement auto-approved!"
                                )
                            else:
                                st.success(
                                    "📬 Sent to teacher for approval!"
                                )

                            st.rerun()

    finally:
        conn.close()