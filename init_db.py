import sqlite3
from contextlib import contextmanager

DB_PATH = "database.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_one(records):
    if isinstance(records, list) and len(records) > 0:
        return records[0]
    return None

def find_by_name(cls, table, name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE name = ?", (name,))
        record = cursor.fetchone()
        if record:
            # Map columns to constructor args using cursor.description
            desc = cursor.description
            kwargs = {desc[i][0]: record[i] for i in range(len(desc))}
            return cls(**kwargs)
        return None
