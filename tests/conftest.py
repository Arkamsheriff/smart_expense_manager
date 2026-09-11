import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.api.auth import get_current_user
from app.database import connection


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"


@pytest.fixture(autouse=True)
def force_sqlite_for_all_tests(monkeypatch, tmp_path):
    """
    Force every test to use an isolated SQLite database.

    This prevents tests from accidentally connecting to the
    Supabase/PostgreSQL production database through .env.
    """

    db_path = tmp_path / "test_expenses.db"

    # Always use SQLite during tests.
    monkeypatch.setenv("USE_POSTGRES", "false")

    # Point the application database connection to this test DB.
    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(db_path)
    )

    # Create the tables required by the application.
    conn = sqlite3.connect(db_path)

    # ---------------------------------------------------------
    # Expenses
    # ---------------------------------------------------------

    conn.execute(
        """
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL,
            user_id TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Income
    # ---------------------------------------------------------

    conn.execute(
        """
        CREATE TABLE incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL,
            user_id TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Budgets
    # ---------------------------------------------------------

    conn.execute(
        """
        CREATE TABLE budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL,
            user_id TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Goals
    # ---------------------------------------------------------

    conn.execute(
        """
        CREATE TABLE goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL DEFAULT 0,
            target_date TEXT,
            created_at TEXT NOT NULL,
            user_id TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Recurring Expenses
    # ---------------------------------------------------------

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
            active INTEGER NOT NULL DEFAULT 1,
            user_id TEXT
        )
        """
    )

    conn.commit()
    conn.close()

    yield db_path


@pytest.fixture
def test_db(force_sqlite_for_all_tests):
    """
    Backward-compatible fixture for tests that explicitly request
    test_db.
    """

    return force_sqlite_for_all_tests


@pytest.fixture
def authenticated_user():
    """
    Return the fake authenticated user used by API tests.
    """

    return {
        "id": TEST_USER_ID,
        "email": "test@example.com",
    }


@pytest.fixture
def client(test_db, authenticated_user):
    """
    Provide a FastAPI TestClient using the isolated SQLite database
    and an authenticated test user.
    """

    def override_get_current_user():
        return authenticated_user

    app.dependency_overrides[get_current_user] = (
        override_get_current_user
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None
        )
