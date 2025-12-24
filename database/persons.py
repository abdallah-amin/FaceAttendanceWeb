import sqlite3
import pickle
import numpy as np
from database.db import get_conn


def get_all_persons():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, encoding FROM persons")
    rows = cur.fetchall()
    conn.close()

    persons = []
    for r in rows:
        persons.append({
            "id": r["id"],
            "name": r["name"],
            "encoding": pickle.loads(r["encoding"])
        })
    return persons


def add_person(name: str, encoding: np.ndarray):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO persons (name, encoding) VALUES (?, ?)",
        (name, pickle.dumps(encoding))
    )

    conn.commit()
    conn.close()


def find_person_by_encoding(new_encoding, tolerance=0.6):
    persons = get_all_persons()

    if not persons:
        return None

    encs = np.array([p["encoding"] for p in persons])
    distances = np.linalg.norm(encs - new_encoding, axis=1)

    best_idx = int(np.argmin(distances))
    if distances[best_idx] < tolerance:
        return persons[best_idx]

    return None
