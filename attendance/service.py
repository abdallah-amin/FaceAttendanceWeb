from datetime import datetime, date

from database.db import get_conn


def today_str():
    return date.today().strftime("%Y-%m-%d")


def mark_attendance(person_id: int):
    """
    تسجيل حضور شخص (مرة واحدة في اليوم)
    """
    conn = get_conn()
    cur = conn.cursor()

    d = today_str()
    t = datetime.now().strftime("%H:%M:%S")

    cur.execute(
        """
        SELECT 1 FROM attendance
        WHERE person_id = ? AND date = ?
        """,
        (person_id, d),
    )

    if cur.fetchone() is None:
        cur.execute(
            """
            INSERT INTO attendance (person_id, date, time)
            VALUES (?, ?, ?)
            """,
            (person_id, d, t),
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def compute_status(target_date: str | None = None):
    """
    جلب الحضور لتاريخ معين
    لو التاريخ مش متحدد → النهارده
    """
    d = target_date or today_str()

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.id, p.name, a.time
        FROM attendance a
        JOIN persons p ON p.id = a.person_id
        WHERE a.date = ?
        ORDER BY a.time
        """,
        (d,),
    )

    rows = cur.fetchall()
    conn.close()

    present = [
        {"id": r["id"], "name": r["name"], "time": r["time"]}
        for r in rows
    ]

    return {
        "date": d,
        "present_count": len(present),
        "present": present,
    }


