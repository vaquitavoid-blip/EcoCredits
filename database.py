import sqlite3
import hashlib

DB = "ecocredits.db"


def get_connection():

    return sqlite3.connect(
        DB,
        check_same_thread=False
    )


def _hash(p):

    return hashlib.sha256(
        p.encode()
    ).hexdigest()


# ─────────────────────────────────────────────
# SUBJECT → TEACHER
# ─────────────────────────────────────────────

SUBJECT_TEACHER_MAP = {

    "Add Maths": "maths_teacher",

    "Extended Maths": "maths_teacher",

    "Physics": "science_teacher",

    "Chemistry": "science_teacher",

    "Biology": "science_teacher",

    "Combined Science": "science_teacher",

    "FLE": "english_teacher",

    "ESL": "english_teacher",

    "Economics": "business_teacher",

    "Business Studies": "business_teacher",

    "Accounting": "business_teacher",

    "ICT": "cs_teacher",

    "DT": "cs_teacher",

    "Art and Design": "arts_teacher",
}


# ─────────────────────────────────────────────
# CATEGORY → TEACHER
# ─────────────────────────────────────────────

CATEGORY_TEACHER_MAP = {

    "Science": "science_teacher",

    "Technology": "cs_teacher",

    "Mathematics": "maths_teacher",

    "Finance": "business_teacher",

    "Creative Arts": "english_teacher",

    "Sports": "class_teacher",

    "Other": "class_teacher",
}


# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────

def setup_database():

    conn = get_connection()

    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT,

        auto_approvals INTEGER DEFAULT 0
    )
    """)

    # SUBJECTS
    c.execute("""
    CREATE TABLE IF NOT EXISTS subjects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        grade TEXT,

        approved INTEGER DEFAULT 0,

        teacher TEXT DEFAULT 'class_teacher',

        image_path TEXT
    )
    """)

    # REPORT CARD QUEUE
    c.execute("""
    CREATE TABLE IF NOT EXISTS report_card_queue(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        image_path TEXT,

        detected_json TEXT,

        status TEXT DEFAULT 'pending',

        assigned_teacher TEXT DEFAULT 'class_teacher'
    )
    """)

    # ACHIEVEMENTS
    c.execute("""
    CREATE TABLE IF NOT EXISTS achievements(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        title TEXT,

        level TEXT,

        category TEXT,

        approved INTEGER DEFAULT 0,

        assigned_teacher TEXT
    )
    """)

    # APPROVAL QUEUE
    c.execute("""
    CREATE TABLE IF NOT EXISTS approval_queue(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        achievement_id INTEGER,

        status TEXT DEFAULT 'pending'
    )
    """)

    # ─────────────────────────────────────────
    # SAFE COLUMN UPGRADES
    # ─────────────────────────────────────────

    safe_alters = [

        (
            "subjects",
            "teacher TEXT DEFAULT 'class_teacher'"
        ),

        (
            "subjects",
            "image_path TEXT"
        ),

        (
            "users",
            "auto_approvals INTEGER DEFAULT 0"
        )
    ]

    for table, col in safe_alters:

        try:

            c.execute(
                f"ALTER TABLE {table} ADD COLUMN {col}"
            )

        except:
            pass

    # ─────────────────────────────────────────
    # DEFAULT ADMIN
    # ─────────────────────────────────────────

    c.execute("""
    INSERT OR IGNORE INTO users(
        id,
        username,
        password,
        role
    )
    VALUES(
        1,
        'admin',
        ?,
        'admin'
    )
    """, (_hash("admin123"),))

    # ─────────────────────────────────────────
    # DEFAULT TEACHERS
    # PASSWORD = t123
    # ─────────────────────────────────────────

    teachers = [

        (2, "class_teacher"),

        (3, "maths_teacher"),

        (4, "science_teacher"),

        (5, "english_teacher"),

        (6, "business_teacher"),

        (7, "cs_teacher"),

        (8, "arts_teacher")
    ]

    for tid, name in teachers:

        c.execute("""
        INSERT OR IGNORE INTO users(
            id,
            username,
            password,
            role
        )
        VALUES(?,?,?,'teacher')
        """, (
            tid,
            name,
            _hash("t123")
        ))

    conn.commit()

    conn.close()