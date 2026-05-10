import sqlite3
import hashlib
from datetime import datetime

DB = "ecocredits.db"


def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)


def _hash(p):
    return hashlib.sha256(p.encode()).hexdigest()


SUBJECT_TEACHER_MAP = {
    "Add Maths":        "maths_teacher",
    "Extended Maths":   "maths_teacher",
    "Combined Science": "science_teacher",
    "Physics":          "science_teacher",
    "Chemistry":        "science_teacher",
    "Biology":          "science_teacher",
    "FLE":              "english_teacher",
    "ESL":              "english_teacher",
    "Literature":       "english_teacher",
    "Economics":        "business_teacher",
    "Business Studies": "business_teacher",
    "Accounting":       "business_teacher",
    "ICT":              "cs_teacher",
    "DT":               "cs_teacher",
    "Art and Design":   "arts_teacher",
    "History":          "class_teacher",
    "Geography":        "class_teacher",
    "Sociology":        "class_teacher",
    "Psychology":       "class_teacher",
}

CATEGORY_TEACHER_MAP = {
    "Science":       "science_teacher",
    "Technology":    "cs_teacher",
    "Mathematics":   "maths_teacher",
    "Finance":       "business_teacher",
    "Creative Arts": "arts_teacher",
    "Sports":        "class_teacher",
    "Other":         "class_teacher",
}

TEACHER_DISPLAY = {
    "class_teacher":    "🏫 Class Teacher",
    "maths_teacher":    "📐 Maths Teacher",
    "science_teacher":  "🔬 Science Teacher",
    "english_teacher":  "📖 English Teacher",
    "business_teacher": "💼 Business Teacher",
    "cs_teacher":       "💻 CS Teacher",
    "arts_teacher":     "🎨 Arts Teacher",
}


def setup_database():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        username         TEXT UNIQUE,
        password         TEXT,
        role             TEXT,
        auto_approvals   INTEGER DEFAULT 0,
        batch_locked     INTEGER DEFAULT 0,
        uploads_today    INTEGER DEFAULT 0,
        last_upload_date TEXT DEFAULT ''
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER,
        subject  TEXT,
        grade    TEXT,
        approved INTEGER DEFAULT 0,
        teacher  TEXT DEFAULT 'class_teacher'
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS report_card_queue(
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id          INTEGER,
        image_path       TEXT,
        detected_json    TEXT,
        status           TEXT DEFAULT 'pending',
        assigned_teacher TEXT DEFAULT 'class_teacher',
        submitted_at     TEXT DEFAULT ''
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS achievements(
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id          INTEGER,
        title            TEXT,
        level            TEXT,
        category         TEXT,
        approved         INTEGER DEFAULT 0,
        assigned_teacher TEXT,
        batch_number     INTEGER DEFAULT 0,
        image_hash       TEXT DEFAULT '',
        submitted_date   TEXT DEFAULT ''
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS approval_queue(
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        achievement_id INTEGER,
        status         TEXT DEFAULT 'pending'
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_log(
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        username  TEXT,
        action    TEXT,
        detail    TEXT
    )""")

    # Safe column upgrades for existing databases
    safe_alters = [
        ("users", "auto_approvals INTEGER DEFAULT 0"),
        ("users", "batch_locked INTEGER DEFAULT 0"),
        ("users", "uploads_today INTEGER DEFAULT 0"),
        ("users", "last_upload_date TEXT DEFAULT ''"),
        ("subjects", "teacher TEXT DEFAULT 'class_teacher'"),
        ("achievements", "batch_number INTEGER DEFAULT 0"),
        ("achievements", "image_hash TEXT DEFAULT ''"),
        ("achievements", "submitted_date TEXT DEFAULT ''"),
        ("report_card_queue", "submitted_at TEXT DEFAULT ''"),
    ]
    for table, col_def in safe_alters:
        try:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
        except Exception:
            pass

    # Default admin
    c.execute("""INSERT OR IGNORE INTO users(id,username,password,role)
                 VALUES(1,'admin',?,'admin')""", (_hash("admin123"),))

    # Default teachers (password: t123)
    teachers = [
        (2, "class_teacher"),
        (3, "maths_teacher"),
        (4, "science_teacher"),
        (5, "english_teacher"),
        (6, "business_teacher"),
        (7, "cs_teacher"),
        (8, "arts_teacher"),
    ]
    for tid, tname in teachers:
        c.execute("""INSERT OR IGNORE INTO users(id,username,password,role)
                     VALUES(?,?,?,'teacher')""", (tid, tname, _hash("t123")))

    conn.commit()
    conn.close()


def write_audit(username, action, detail=""):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO audit_log(timestamp,username,action,detail) VALUES(?,?,?,?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username, action, detail)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def check_and_reset_upload_count(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    c = conn.cursor()
    row = c.execute(
        "SELECT uploads_today, last_upload_date FROM users WHERE id=?",
        (user_id,)
    ).fetchone()
    if row and row[1] != today:
        c.execute(
            "UPDATE users SET uploads_today=0, last_upload_date=? WHERE id=?",
            (today, user_id)
        )
        conn.commit()
    conn.close()


def get_upload_count(user_id):
    check_and_reset_upload_count(user_id)
    conn = get_connection()
    c = conn.cursor()
    row = c.execute(
        "SELECT uploads_today FROM users WHERE id=?", (user_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else 0


def increment_upload_count(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE users SET uploads_today=uploads_today+1, last_upload_date=? WHERE id=?",
        (today, user_id)
    )
    conn.commit()
    conn.close()