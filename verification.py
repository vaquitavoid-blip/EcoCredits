from database import get_connection

def get_pending():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM achievements WHERE status='pending'")
    data = c.fetchall()

    conn.close()
    return data

def approve(id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE achievements SET status='approved' WHERE id=?", (id,))
    conn.commit()

    # 🔍 DEBUG CHECK (VERY IMPORTANT)
    c.execute("SELECT status FROM achievements WHERE id=?", (id,))
    print("AFTER UPDATE:", c.fetchone())

    conn.close()