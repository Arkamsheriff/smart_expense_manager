from datetime import datetime
import sqlite3

from app.database.connection import get_connection
from app.budget.budget import Budget


class BudgetRepository:

    def initialize_table(self):
        connection = get_connection()

        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT NOT NULL UNIQUE,
                    amount REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            connection.commit()

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def add(self, budget):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO budgets (
                    month,
                    amount,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    budget.month,
                    budget.amount,
                    budget.created_at.isoformat()
                )
            )

            budget.id = cursor.lastrowid

            connection.commit()

            return budget

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def get_by_month(self, month):
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    id,
                    month,
                    amount,
                    created_at
                FROM budgets
                WHERE month = ?
                """,
                (month,)
            ).fetchone()

            if row is None:
                return None

            return Budget(
                row["id"],
                row["month"],
                row["amount"],
                datetime.fromisoformat(row["created_at"])
            )

        finally:
            connection.close()

    def get_all(self):
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    id,
                    month,
                    amount,
                    created_at
                FROM budgets
                ORDER BY month
                """
            ).fetchall()

            return [
                Budget(
                    row["id"],
                    row["month"],
                    row["amount"],
                    datetime.fromisoformat(row["created_at"])
                )
                for row in rows
            ]

        finally:
            connection.close()

    def update(self, budget):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE budgets
                SET month = ?,
                    amount = ?
                WHERE id = ?
                """,
                (
                    budget.month,
                    budget.amount,
                    budget.id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def delete(self, budget_id):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM budgets
                WHERE id = ?
                """,
                (budget_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()