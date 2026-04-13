import sqlite3

DB_PATH = "data/md_radar.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        keyword TEXT,
        name TEXT,
        price TEXT,
        mall TEXT,
        link TEXT,
        collected_at TEXT
    )
    """)

    conn.commit()
    conn.close()
