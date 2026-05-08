import streamlit as st
import pandas as pd
import hashlib
from database import get_connection


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


def admin_panel():
    st.title("🛡️ Admin God Mode")
    st.caption("Full control over all users, subjects, achievements and the approval queue.")

    conn = get_connection()
    c = conn.cursor()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Users",
        "📚 Subjects",
        "🏆 Achievements",
        "📋 Queue",
        "💣 Danger Zone"
    ])

    # ── TAB 1: Users ──────────────────────────────────────────────────────────
    with tab1:
        st.subheader("All Users")
        users = c.execute(
            "SELECT id, username, role, auto_approvals FROM users"
        ).fetchall()
        user_df = pd.DataFrame(users, columns=["ID", "Username", "Role", "Auto-Approvals"])
        st.dataframe(user_df, use_container_width=True, hide_index=True)

        st.divider()
        usernames = [u[1] for u in users]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Change Role")
            sel_user = st.selectbox("User", usernames, key="role_user")
            new_role = st.selectbox("New Role", ["student", "teacher", "admin"])
            if st.button("Update Role", type="primary"):
                c.execute("UPDATE users SET role=? WHERE username=?", (new_role, sel_user))
                conn.commit()
                st.success(f"✅ {sel_user} → {new_role}")
                st.rerun()

        with col2:
            st.subheader("Reset Password")
            sel_user2 = st.selectbox("User", usernames, key="pw_user")
            new_pw = st.text_input("New Password", type="password")
            if st.button("Reset Password", type="primary"):
                if new_pw:
                    c.execute(
                        "UPDATE users SET password=? WHERE username=?",
                        (hash_password(new_pw), sel_user2)
                    )
                    conn.commit()
                    st.success("✅ Password updated")
                else:
                    st.error("Enter a password")

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Add User")
            new_uname = st.text_input("Username", key="add_uname")
            new_upw = st.text_input("Password", type="password", key="add_upw")
            new_urole = st.selectbox("Role", ["student", "teacher", "admin"], key="add_urole")
            if st.button("➕ Create User", type="primary"):
                try:
                    c.execute(
                        "INSERT INTO users(username, password, role) VALUES(?,?,?)",
                        (new_uname, hash_password(new_upw), new_urole)
                    )
                    conn.commit()
                    st.success(f"✅ Created {new_uname}")
                    st.rerun()
                except Exception:
                    st.error("Username already exists")

        with col4:
            st.subheader("Reset Auto-Approval Counter")
            sel_reset = st.selectbox("User", usernames, key="reset_auto")
            if st.button("🔄 Reset Counter"):
                c.execute("UPDATE users SET auto_approvals=0 WHERE username=?", (sel_reset,))
                conn.commit()
                st.success("✅ Counter reset to 0")
                st.rerun()

        st.divider()
        st.subheader("Delete User")
        deletable = [u[1] for u in users if u[1] != "admin"]
        if deletable:
            del_user = st.selectbox("User to delete", deletable, key="del_user")
            if st.button("🗑️ Delete User + All Their Data", type="primary"):
                uid = c.execute("SELECT id FROM users WHERE username=?", (del_user,)).fetchone()[0]
                c.execute("DELETE FROM users WHERE id=?", (uid,))
                c.execute("DELETE FROM subjects WHERE user_id=?", (uid,))
                c.execute("DELETE FROM achievements WHERE user_id=?", (uid,))
                conn.commit()
                st.success(f"✅ Deleted {del_user}")
                st.rerun()

    # ── TAB 2: Subjects ───────────────────────────────────────────────────────
    with tab2:
        st.subheader("All Subject Records")
        subjects = c.execute("""
            SELECT subjects.id, users.username, subjects.subject,
                   subjects.grade, subjects.approved
            FROM subjects JOIN users ON subjects.user_id = users.id
        """).fetchall()

        if subjects:
            sub_df = pd.DataFrame(
                subjects,
                columns=["ID", "Student", "Subject", "Grade", "Approved"]
            )
            sub_df["Approved"] = sub_df["Approved"].replace({0: "No", 1: "Yes"})
            st.dataframe(sub_df, use_container_width=True, hide_index=True)

            st.divider()
            col1, col2 = st.columns(2)
            record_ids = [str(s[0]) for s in subjects]

            with col1:
                st.subheader("Edit Grade")
                sel_id = st.selectbox("Record ID", record_ids, key="edit_grade_id")
                new_grade = st.selectbox("New Grade", ["A*", "A", "B", "C", "D"])
                if st.button("✏️ Update Grade", type="primary"):
                    c.execute("UPDATE subjects SET grade=? WHERE id=?", (new_grade, int(sel_id)))
                    conn.commit()
                    st.success("✅ Grade updated")
                    st.rerun()

            with col2:
                st.subheader("Delete Record")
                del_sub = st.selectbox("Record ID", record_ids, key="del_sub")
                if st.button("🗑️ Delete Record", type="primary"):
                    c.execute("DELETE FROM subjects WHERE id=?", (int(del_sub),))
                    conn.commit()
                    st.success("✅ Deleted")
                    st.rerun()
        else:
            st.info("No subject records yet.")

    # ── TAB 3: Achievements ───────────────────────────────────────────────────
    with tab3:
        st.subheader("All Achievements")
        achievements = c.execute("""
            SELECT achievements.id, users.username, achievements.title,
                   achievements.level, achievements.category,
                   achievements.approved, achievements.assigned_teacher
            FROM achievements JOIN users ON achievements.user_id = users.id
        """).fetchall()

        if achievements:
            ach_df = pd.DataFrame(
                achievements,
                columns=["ID", "Student", "Title", "Level", "Category", "Approved", "Teacher"]
            )
            ach_df["Approved"] = ach_df["Approved"].replace({0: "⏳ Pending", 1: "✅ Approved"})
            st.dataframe(ach_df, use_container_width=True, hide_index=True)

            st.divider()
            ach_ids = [str(a[0]) for a in achievements]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Approve / Reject")
                sel_ach = st.selectbox("Achievement ID", ach_ids, key="ach_approve")
                a1, a2 = st.columns(2)
                with a1:
                    if st.button("✅ Approve"):
                        c.execute("UPDATE achievements SET approved=1 WHERE id=?", (int(sel_ach),))
                        c.execute("UPDATE approval_queue SET status='approved' WHERE achievement_id=?", (int(sel_ach),))
                        conn.commit()
                        st.success("Approved")
                        st.rerun()
                with a2:
                    if st.button("❌ Reject"):
                        c.execute("DELETE FROM achievements WHERE id=?", (int(sel_ach),))
                        c.execute("DELETE FROM approval_queue WHERE achievement_id=?", (int(sel_ach),))
                        conn.commit()
                        st.error("Rejected")
                        st.rerun()

            with col2:
                st.subheader("Override Level")
                sel_ach2 = st.selectbox("Achievement ID", ach_ids, key="ach_level")
                new_level = st.selectbox(
                    "New Level",
                    ["School", "District", "State", "National", "International"]
                )
                if st.button("✏️ Set Level", type="primary"):
                    c.execute("UPDATE achievements SET level=? WHERE id=?", (new_level, int(sel_ach2)))
                    conn.commit()
                    st.success("✅ Level updated")
                    st.rerun()

            with col3:
                st.subheader("Override Category")
                sel_ach3 = st.selectbox("Achievement ID", ach_ids, key="ach_cat")
                new_cat = st.selectbox(
                    "New Category",
                    ["Science", "Technology", "Mathematics", "Finance", "Creative Arts", "Sports", "Other"]
                )
                if st.button("✏️ Set Category", type="primary"):
                    c.execute("UPDATE achievements SET category=? WHERE id=?", (new_cat, int(sel_ach3)))
                    conn.commit()
                    st.success("✅ Category updated")
                    st.rerun()
        else:
            st.info("No achievements yet.")

    # ── TAB 4: Queue ─────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Approval Queue")
        queue = c.execute("""
            SELECT approval_queue.id, users.username, achievements.title,
                   achievements.level, achievements.category,
                   achievements.assigned_teacher, approval_queue.status
            FROM approval_queue
            JOIN achievements ON approval_queue.achievement_id = achievements.id
            JOIN users ON achievements.user_id = users.id
        """).fetchall()

        if queue:
            q_df = pd.DataFrame(
                queue,
                columns=["Queue ID", "Student", "Title", "Level", "Category", "Teacher", "Status"]
            )
            st.dataframe(q_df, use_container_width=True, hide_index=True)
            st.metric("Total pending", len([q for q in queue if q[6] == "pending"]))
        else:
            st.success("✅ Queue is empty.")

    # ── TAB 5: Danger Zone ────────────────────────────────────────────────────
    with tab5:
        st.error("⚠️ All actions below are permanent and cannot be undone.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear ALL Subjects"):
                c.execute("DELETE FROM subjects")
                conn.commit()
                st.warning("All subject records deleted.")

            if st.button("🗑️ Clear ALL Achievements"):
                c.execute("DELETE FROM achievements")
                c.execute("DELETE FROM approval_queue")
                conn.commit()
                st.warning("All achievements and queue deleted.")

        with col2:
            if st.button("🗑️ Clear ALL Student Accounts"):
                c.execute("DELETE FROM subjects WHERE user_id IN (SELECT id FROM users WHERE role='student')")
                c.execute("DELETE FROM achievements WHERE user_id IN (SELECT id FROM users WHERE role='student')")
                c.execute("DELETE FROM users WHERE role='student'")
                conn.commit()
                st.warning("All student accounts deleted.")

            if st.button("🔄 Reset All Auto-Approval Counters"):
                c.execute("UPDATE users SET auto_approvals=0")
                conn.commit()
                st.success("All counters reset.")

        st.markdown("---")
        st.subheader("💣 Full Database Reset")
        confirm = st.text_input("Type **RESET** to confirm full wipe")
        if st.button("💣 Execute Full Reset", type="primary"):
            if confirm == "RESET":
                for tbl in ["subjects", "achievements", "approval_queue"]:
                    c.execute(f"DELETE FROM {tbl}")
                c.execute("DELETE FROM users WHERE role != 'admin'")
                c.execute("UPDATE users SET auto_approvals=0")
                conn.commit()
                st.success("✅ Full reset complete. Admin accounts kept.")
            else:
                st.error("Type RESET exactly to confirm.")

    conn.close()