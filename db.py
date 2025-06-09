import sqlite3
from datetime import date
from typing import Iterable, Optional, List

DB_PATH = 'experiments.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    intervention TEXT NOT NULL,
    dose TEXT,
    mood INTEGER,
    focus INTEGER,
    sleep_quality INTEGER,
    heart_rate REAL,
    sleep_hours REAL,
    notes TEXT,
    tags TEXT
);
"""

def get_conn(path: str = DB_PATH):
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn

def init_db(conn=None):
    if conn is None:
        conn = get_conn()
    conn.execute(SCHEMA)
    conn.commit()


def add_entry(
    intervention: str,
    dose: str,
    date_value: Optional[date] = None,
    mood: Optional[int] = None,
    focus: Optional[int] = None,
    sleep_quality: Optional[int] = None,
    heart_rate: Optional[float] = None,
    sleep_hours: Optional[float] = None,
    notes: str = "",
    tags: Optional[Iterable[str]] = None,
    conn=None,
):
    if conn is None:
        conn = get_conn()
    if date_value is None:
        date_value = date.today()
    tags_text = ",".join(tags) if tags else ""
    conn.execute(
        "INSERT INTO entries (date, intervention, dose, mood, focus, sleep_quality, heart_rate, sleep_hours, notes, tags)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            date_value.isoformat(),
            intervention,
            dose,
            mood,
            focus,
            sleep_quality,
            heart_rate,
            sleep_hours,
            notes,
            tags_text,
        ),
    )
    conn.commit()


def fetch_entries(
    tag: Optional[str] = None,
    intervention: Optional[str] = None,
    conn=None,
):
    if conn is None:
        conn = get_conn()
    query = "SELECT * FROM entries"
    params: List[str] = []
    clauses = []
    if tag:
        clauses.append("tags LIKE ?")
        params.append(f"%{tag}%")
    if intervention:
        clauses.append("intervention = ?")
        params.append(intervention)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY date DESC"
    cur = conn.execute(query, params)
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    init_db()
