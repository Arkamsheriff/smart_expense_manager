import sqlite3
from datetime import datetime

from app.database.connection import get_connection
from app.income.income import Income


class IncomeRepository:

    def initialize_table(self):
        connection = get_connection()

        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS incomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            connection.commit()

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def add(self, income):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO incomes (
                    description,
                    amount,
                    category,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    income.description,
                    income.amount,
                    income.category,
                    income.created_at.isoformat()
                )
            )

            income.id = cursor.lastrowid

            connection.commit()

            return income

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def get_by_id(self, income_id):
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT id, description, amount, category, created_at
                FROM incomes
                WHERE id = ?
                """,
                (income_id,)
            ).fetchone()

            if row is None:
                return None

            return self._convert_row_to_income(row)

        finally:
            connection.close()

    def get_all(self):
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT id, description, amount, category, created_at
                FROM incomes
                ORDER BY id
                """
            ).fetchall()

            return self._convert_rows_to_incomes(rows)

        finally:
            connection.close()

    def update(self, income):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE incomes
                SET description = ?,
                    amount = ?,
                    category = ?
                WHERE id = ?
                """,
                (
                    income.description,
                    income.amount,
                    income.category,
                    income.id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def delete(self, income_id):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM incomes
                WHERE id = ?
                """,
                (income_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    def total(self):
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                AS total
                FROM incomes
                """
            ).fetchone()

            return row["total"]

        finally:
            connection.close()

    def get_by_category(self, category):
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT id, description, amount, category, created_at
                FROM incomes
                WHERE LOWER(category) = LOWER(?)
                ORDER BY created_at DESC
                """,
                (category,)
            ).fetchall()

            return self._convert_rows_to_incomes(rows)

        finally:
            connection.close()

    def _convert_row_to_income(self, row):
        return Income(
            row["id"],
            row["description"],
            row["amount"],
            row["category"],
            datetime.fromisoformat(row["created_at"])
        )

    def _convert_rows_to_incomes(self, rows):
        return [
            self._convert_row_to_income(row)
            for row in rows
        ]