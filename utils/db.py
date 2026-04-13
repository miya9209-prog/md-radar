import sqlite3
from pathlib import Path

def _get_db_path() -> Path:
    data_dir = Path.home() / ".md_radar_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "md_radar.db"

DB_PATH = _get_db_path()

def get_conn():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

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
        collected_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        status TEXT,
        message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_products(rows):
    if not rows:
        return 0
    conn = get_conn()
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT INTO products (source, keyword, name, price, mall, link)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count

def get_recent_products(limit=300, source=None):
    conn = get_conn()
    cur = conn.cursor()
    if source:
        cur.execute(
            """
            SELECT id, source, keyword, name, price, mall, link, collected_at
            FROM products
            WHERE source = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (source, limit),
        )
    else:
        cur.execute(
            """
            SELECT id, source, keyword, name, price, mall, link, collected_at
            FROM products
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_names_for_insight(limit=120):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name
        FROM products
        WHERE name IS NOT NULL AND TRIM(name) != ''
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def get_summary_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    total = cur.fetchone()[0]
    cur.execute("SELECT source, COUNT(*) FROM products GROUP BY source ORDER BY COUNT(*) DESC")
    by_source = cur.fetchall()
    cur.execute("SELECT mall, COUNT(*) FROM products GROUP BY mall ORDER BY COUNT(*) DESC LIMIT 20")
    by_mall = cur.fetchall()
    conn.close()
    return {"total": total, "by_source": by_source, "by_mall": by_mall}

def log_event(source, status, message):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (source, status, message) VALUES (?, ?, ?)",
        (source, status, message),
    )
    conn.commit()
    conn.close()

def get_db_path_text():
    return str(DB_PATH)
