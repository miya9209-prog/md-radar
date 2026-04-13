import sqlite3
from pathlib import Path
import streamlit as st

def _get_db_path() -> Path:
    # Streamlit Cloud의 소스 디렉터리(/mount/src)는 쓰기 제한이 있을 수 있으므로
    # 항상 사용자 홈 아래 writable 경로를 사용합니다.
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
        collected_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS collection_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        status TEXT,
        message TEXT,
        collected_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_products(rows):
    if not rows:
        return 0
    conn = get_conn()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO products (source, keyword, name, price, mall, link, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, rows)
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count

def get_recent_products(limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source, keyword, name, price, mall, link, collected_at
        FROM products
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_product_names(limit=50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT name
        FROM products
        WHERE name IS NOT NULL AND TRIM(name) != ''
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def log_event(source, status, message=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO collection_logs (source, status, message)
        VALUES (?, ?, ?)
    """, (source, status, message))
    conn.commit()
    conn.close()

def get_db_location_text():
    return str(DB_PATH)
