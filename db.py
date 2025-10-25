import sqlite3

def get_db():
    conn = sqlite3.connect("images.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
    id TEXT PRIMARY KEY,
    image_url TEXT NOT NULL,
    user_id TEXT
    )
    """)
    conn.commit()
    conn.close()
