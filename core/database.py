import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/expenses.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(title: str, amount: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses (title, amount, created_at) VALUES (?, ?, ?)",
        (title, amount, datetime.now().isoformat())
    )

    expense_id = cur.lastrowid
    conn.commit()
    conn.close()

    return expense_id


def get_all_expenses():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, amount, created_at FROM expenses ORDER BY id ASC"
    )

    rows = cur.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
