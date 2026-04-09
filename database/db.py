import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(__file__), "..", "spendly.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables. Safe to call multiple times."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development. Idempotent — skips if data already exists."""
    conn = get_db()

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 350.00,  "Food",          "2026-04-01", "Lunch at cafe"),
        (user_id, 120.00,  "Transport",     "2026-04-02", "Metro card recharge"),
        (user_id, 1200.00, "Bills",         "2026-04-03", "Electricity bill"),
        (user_id, 800.00,  "Health",        "2026-04-04", "Pharmacy"),
        (user_id, 499.00,  "Entertainment", "2026-04-05", "Movie ticket"),
        (user_id, 1999.00, "Shopping",      "2026-04-06", "New T-shirt"),
        (user_id, 250.00,  "Other",         "2026-04-07", "Miscellaneous"),
        (user_id, 60.00,   "Food",          "2026-04-09", "Tea and snacks"),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()
