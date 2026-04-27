import sqlite3
import time
import os

DB_PATH = "storage/tools/convert_ttf/meta/convert_ttf_meta.db"
os.makedirs("storage", exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

def add_file(file_id: str, name: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO files (file_id, name, created_at)
        VALUES (?, ?, ?)
    """, (file_id, name, int(time.time())))

    conn.commit()
    conn.close()


def get_file(file_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM files WHERE file_id = ?
    """, (file_id,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

# def cleanup(ttl_seconds: int = 3600):
#     conn = get_conn()
#     cur = conn.cursor()

#     cutoff = int(time.time()) - ttl_seconds

#     cur.execute("""
#         SELECT file_id FROM files WHERE created_at < ?
#     """, (cutoff,))

#     old_files = cur.fetchall()

#     cur.execute("""
#         DELETE FROM files WHERE created_at < ?
#     """, (cutoff,))

#     conn.commit()
#     conn.close()

#     return [f["file_id"] for f in old_files]

def cleanup():
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        DELETE FROM files
    """)

    conn.commit()
    conn.close()