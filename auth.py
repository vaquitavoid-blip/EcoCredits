import hashlib
from database import get_connection, write_audit


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
        write_audit(username, "REGISTER", "New student account")
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
    if user:
        write_audit(username, "LOGIN", f"Role: {user[3]}")
    return user