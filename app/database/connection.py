import os
import sqlite3

from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row


load_dotenv()

DATABASE_PATH = "data/expenses.db"
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000000"


def get_connection():
    """
    Return a database connection.

    SQLite is used by default for local development and tests.
    PostgreSQL is used when USE_POSTGRES=true.
    """

    use_postgres = os.getenv("USE_POSTGRES", "false").lower() == "true"

    if use_postgres:
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError(
                "DATABASE_URL is required when USE_POSTGRES=true"
            )

        return psycopg.connect(
            database_url,
            row_factory=dict_row
        )

    directory = os.path.dirname(DATABASE_PATH)

    if directory:
        os.makedirs(directory, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection