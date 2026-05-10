import streamlit as st
import pandas as pd
import hashlib
from database import get_connection, write_audit


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


def admin_panel():
    st.markdown(
        "<h1 style='font-family:Orbitron,monospace;color:#00d4ff;"
        "text-shadow:0 0 20px rgba(0,212,255,0.5);'>🛡️ ADMIN CONTROL</h1>",
        unsafe_allow_html=True
    )
    st.caption("Full system control — every action is logged to the audit trail.")
    st.markdown("---")

    conn = get_connection()
    c    = conn.cursor()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👥 Users",
        "📚 Subjects",
        "🏆 Achievements",
        "📋 Queue",
        "📜 Audit Log",
        "💣 Danger Zone",
    ])

    # ── USERS ────────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("All Users")
        users = c.execute(
            "SELECT id, username, role, auto_approvals, batch_locked, uploads_today FROM users"
        ).fetchall()
        df = pd.DataFrame(
            users,
            columns=["ID","Username","Role","Auto-Approvals","Batch Locked","Uploads Today"]
        )
        df["Batch Locked"] = df["Batch Locked"].replace({0:"No", 1:"🔒 Yes"})
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        usernames = [u[1] for u in users]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Change Role")
            sel  = st.selectbox("User", usernames, key="role_user")
            role = st.selectbox("New Role", ["student","teacher","admin"])
            if st.button("Update Role", type="primary", key="upd_role"):
                c.execute("UPDATE users SET role=? WHERE username=?", (role, sel))
                conn.commit()
                write_audit("admin", "ROLE_CHANGE", f"{sel} → {role}")
                st.success(f"✅ {sel} → {role}")
                st.rerun()

        with col2:
            st.subheader("Reset Password")
            sel2   = st.selectbox("User", usernames, key="pw_user")
            new_pw = st.text_input("New Password", type="password")
            if st.button("Reset Password", type="primary", key="upd_pw"):
                if new_pw:
                    c.execute("UPDATE users SET password=? WHERE username=?",
                              (hash_password(new_pw), sel2))
                    conn.commit()
                    write_audit("admin", "PASSWORD_RESET", sel2)
                    st.success("✅ Password updated")
                else:
                    st.error("Enter a password")

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Add User")
            nu = st.text_input("Username", key="add_uname")
            np = st.text_input("Password", type="password", key="add_upw")
            nr = st.selectbox("Role", ["student","teacher","admin"], key="add_urole")
            if st.button("➕ Create User", type="primary", key="create_user"):
                try:
                    c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",
                              (nu, hash_password(np), nr))
                    conn.commit()
                    write_audit("admin", "CREATE_USER", f"{nu} ({nr})")
                    st.success(f"✅ Created {nu}")
                    st.rerun()
                except Exception:
                    st.error("Username already exists")

        with col4:
            st.subheader("Unlock / Reset")
            sel_u = st.selectbox("User", usernames, key="unlock_user")
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("🔓 Unlock", key="unlock_batch"):
                    c.execute("UPDATE users SET batch_locked=0 WHERE username=?", (sel_u,))
                    conn.commit()
                    write_audit("admin", "BATCH_UNLOCK", sel_u)
                    st.success("Unlocked")
                    st.rerun()
            with b2:
                if st.button("🔄 Counter", key="reset_counter"):
                    c.execute("UPDATE users SET auto_approvals=0 WHERE username=?", (sel_u,))
                    conn.commit()
                    write_audit("admin", "COUNTER_RESET", sel_u)
                    st.success("Reset")
                    st.rerun()
            with b3:
                if st.button("📤 Uploads", key="reset_uploads"):
                    c.execute("UPDATE users SET uploads_today=0 WHERE username=?", (sel_u,))
                    conn.commit()
                    write_audit("admin", "UPLOAD_RESET", sel_u)
                    st.success("Reset")
                    st.rerun()

        st.divider()
        st.subheader("Delete User")
        deletable = [u[1] for u in users if u[1] != "admin"]
        if deletable:
            del_u = st.selectbox("User to delete", deletable, key="del_user")
            if st.button("🗑️ Delete User + All Data", type="primary", key="del_usr_btn"):
                uid = c.execute("SELECT id FROM users WHERE username=?", (del_u,)).fetchone()[0]
                for tbl in ["subjects","achievements"]:
                    c.execute(f"DELETE FROM {tbl} WHERE user_id=?", (uid,))
                c.execute("DELETE FROM users WHERE id=?", (uid,))
                conn.commit()
                write_audit("admin", "DELETE_USER", del_u)
                st.success(f"✅ Deleted {del_u}")
                st.rerun()

    # ── SUBJECTS ─────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("All Subject Records")
        subjects = c.execute("""
            SELECT s.id, u.username, s.subject, s.grade, s.approved, s.teacher
            FROM subjects s JOIN users u ON s.user_id=u.id
        """).fetchall()

        if subjects:
            sdf = pd.DataFrame(subjects, columns=["ID","Student","Subject","Grade","Approved","Teacher"])
            sdf["Approved"] = sdf["Approved"].replace({0:"No", 1:"✅ Yes"})
            st.dataframe(sdf, use_container_width=True, hide_index=True)

            st.divider()
            rids = [str(s[0]) for s in subjects]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Edit Grade")
                sid = st.selectbox("Record ID", rids, key="edit_grade_id")
                ng  = st.selectbox("New Grade", ["A*","A","B","C","D"])
                if st.button("✏️ Update Grade", type="primary", key="upd_grade"):
                    c.execute("UPDATE subjects SET grade=? WHERE id=?", (ng, int(sid)))
                    conn.commit()
                    write_audit("admin", "GRADE_EDIT", f"Record {sid} → {ng}")
                    st.success("✅ Updated")
                    st.rerun()
            with col2:
                st.subheader("Delete Record")
                dsid = st.selectbox("Record ID", rids, key="del_sub")
                if st.button("🗑️ Delete", type="primary", key="del_sub_btn"):
                    c.execute("DELETE FROM subjects WHERE id=?", (int(dsid),))
                    conn.commit()
                    write_audit("admin", "SUBJECT_DELETE", f"Record {dsid}")
                    st.success("✅ Deleted")
                    st.rerun()
        else:
            st.info("No subject records yet.")

    # ── ACHIEVEMENTS ──────────────────────────────────────────────────────────
    with tab3:
        st.subheader("All Achievements")
        achievements = c.execute("""
            SELECT a.id, u.username, a.title, a.level,
                   a.category, a.approved, a.assigned_teacher, a.submitted_date
            FROM achievements a JOIN users u ON a.user_id=u.id
            ORDER BY a.id DESC
        """).fetchall()

        if achievements:
            adf = pd.DataFrame(
                achievements,
                columns=["ID","Student","Title","Level","Category","Approved","Teacher","Date"]
            )
            adf["Approved"] = adf["Approved"].replace({0:"⏳ Pending", 1:"✅ Approved"})
            st.dataframe(adf, use_container_width=True, hide_index=True)

            st.divider()
            aids = [str(a[0]) for a in achievements]
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Approve / Reject")
                sa  = st.selectbox("Achievement ID", aids, key="ach_approve")
                a1, a2 = st.columns(2)
                with a1:
                    if st.button("✅ Approve", key="ach_app_admin"):
                        c.execute("UPDATE achievements SET approved=1 WHERE id=?", (int(sa),))
                        c.execute("UPDATE approval_queue SET status='approved' WHERE achievement_id=?", (int(sa),))
                        conn.commit()
                        write_audit("admin", "ACHIEVEMENT_APPROVE", f"ID {sa}")
                        st.success("Approved")
                        st.rerun()
                with a2:
                    if st.button("❌ Reject", key="ach_rej_admin"):
                        c.execute("DELETE FROM achievements WHERE id=?", (int(sa),))
                        c.execute("DELETE FROM approval_queue WHERE achievement_id=?", (int(sa),))
                        conn.commit()
                        write_audit("admin", "ACHIEVEMENT_REJECT", f"ID {sa}")
                        st.error("Rejected")
                        st.rerun()

            with col2:
                st.subheader("Override Level")
                sa2 = st.selectbox("Achievement ID", aids, key="ach_level")
                nl  = st.selectbox("Level", ["School","District","State","National","International"])
                if st.button("✏️ Set Level", type="primary", key="set_lvl"):
                    c.execute("UPDATE achievements SET level=? WHERE id=?", (nl, int(sa2)))
                    conn.commit()
                    write_audit("admin", "LEVEL_OVERRIDE", f"ID {sa2} → {nl}")
                    st.success("✅ Updated")
                    st.rerun()

            with col3:
                st.subheader("Override Category")
                sa3 = st.selectbox("Achievement ID", aids, key="ach_cat")
                nc  = st.selectbox("Category", ["Science","Technology","Mathematics","Finance","Creative Arts","Sports","Other"])
                if st.button("✏️ Set Category", type="primary", key="set_cat"):
                    c.execute("UPDATE achievements SET category=? WHERE id=?", (nc, int(sa3)))
                    conn.commit()
                    write_audit("admin", "CATEGORY_OVERRIDE", f"ID {sa3} → {nc}")
                    st.success("✅ Updated")
                    st.rerun()
        else:
            st.info("No achievements yet.")

    # ── QUEUE ─────────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Approval Queue")
        queue = c.execute("""
            SELECT aq.id, u.username, a.title, a.level,
                   a.category, a.assigned_teacher, aq.status
            FROM approval_queue aq
            JOIN achievements a ON aq.achievement_id=a.id
            JOIN users u ON a.user_id=u.id
            ORDER BY aq.id DESC
        """).fetchall()

        if queue:
            qdf = pd.DataFrame(
                queue,
                columns=["Queue ID","Student","Title","Level","Category","Teacher","Status"]
            )
            st.dataframe(qdf, use_container_width=True, hide_index=True)
            st.metric("Pending", len([q for q in queue if q[6]=="pending"]))
        else:
            st.success("✅ Queue is empty.")

    # ── AUDIT LOG ─────────────────────────────────────────────────────────────
    with tab5:
        st.subheader("System Audit Log")
        logs = c.execute(
            "SELECT timestamp, username, action, detail FROM audit_log ORDER BY id DESC LIMIT 300"
        ).fetchall()
        if logs:
            ldf = pd.DataFrame(logs, columns=["Timestamp","User","Action","Detail"])
            st.dataframe(ldf, use_container_width=True, hide_index=True)
            st.caption(f"Showing last {len(logs)} entries.")
        else:
            st.info("No audit entries yet.")
        if st.button("🗑️ Clear Audit Log"):
            c.execute("DELETE FROM audit_log")
            conn.commit()
            st.warning("Audit log cleared.")
            st.rerun()

    # ── DANGER ZONE ───────────────────────────────────────────────────────────
    with tab6:
        st.error("⚠️ All actions below are permanent and cannot be undone.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear ALL Subjects"):
                c.execute("DELETE FROM subjects")
                conn.commit()
                write_audit("admin","DANGER_CLEAR_SUBJECTS","")
                st.warning("All subjects deleted.")
            if st.button("🗑️ Clear ALL Achievements"):
                c.execute("DELETE FROM achievements")
                c.execute("DELETE FROM approval_queue")
                conn.commit()
                write_audit("admin","DANGER_CLEAR_ACHIEVEMENTS","")
                st.warning("All achievements deleted.")
        with col2:
            if st.button("🗑️ Clear ALL Students"):
                for tbl in ["subjects","achievements"]:
                    c.execute(f"DELETE FROM {tbl} WHERE user_id IN (SELECT id FROM users WHERE role='student')")
                c.execute("DELETE FROM users WHERE role='student'")
                conn.commit()
                write_audit("admin","DANGER_CLEAR_STUDENTS","")
                st.warning("All students deleted.")
            if st.button("🔄 Reset All Counters"):
                c.execute("UPDATE users SET auto_approvals=0, batch_locked=0, uploads_today=0")
                conn.commit()
                write_audit("admin","DANGER_RESET_COUNTERS","")
                st.success("All counters reset.")

        st.markdown("---")
        st.subheader("💣 Full Database Reset")
        confirm = st.text_input("Type RESET to confirm")
        if st.button("💣 Execute Full Reset", type="primary"):
            if confirm == "RESET":
                for tbl in ["subjects","achievements","approval_queue",
                            "report_card_queue","audit_log"]:
                    c.execute(f"DELETE FROM {tbl}")
                c.execute("DELETE FROM users WHERE role='student'")
                c.execute("UPDATE users SET auto_approvals=0, batch_locked=0, uploads_today=0")
                conn.commit()
                write_audit("admin","FULL_RESET","Database wiped")
                st.success("✅ Full reset complete. Admin + teacher accounts kept.")
            else:
                st.error("Type RESET exactly to confirm.")

    conn.close()