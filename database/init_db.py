from database.db import get_conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # جدول الأشخاص (encoding فقط)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        encoding BLOB NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # جدول الحضور
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY(person_id) REFERENCES persons(id)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
