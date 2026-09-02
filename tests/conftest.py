import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.database import connection


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """
    Create an isolated SQLite database for API tests.

    The real data/expenses.db database is never used by these tests.
    """

    db_path = tmp_path / "test_expenses.db"

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(db_path)
    )

    conn = sqlite3.connect(db_path)

    # Expenses table
    conn.execute(
        """
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Income table
    # IMPORTANT:
    # The application repository uses the table name "incomes".
    conn.execute(
        """
        CREATE TABLE incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Budgets table
    conn.execute(
        """
        CREATE TABLE budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Goals table
    conn.execute(
        """
        CREATE TABLE goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL DEFAULT 0,
            target_date TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    # Recurring expenses table
    conn.execute(
        """
        CREATE TABLE recurring_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            frequency TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            active INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    conn.commit()
    conn.close()

    yield db_path


@pytest.fixture
def client(test_db):
    """
    Provide a FastAPI TestClient using the isolated test database.
    """

    with TestClient(app) as test_client:
        yield test_client