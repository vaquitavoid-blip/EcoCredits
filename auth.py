import hashlib
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username, hash_password(password), "student")
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    user = c.fetchone()
    conn.close()
    return user