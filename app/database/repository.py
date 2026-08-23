from datetime import datetime

from app.database.connection import get_connection
from app.expense import Expense


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


class ExpenseRepository:

    def add(self, expense):
        connection = get_connection()

        cursor = connection.execute(
            """
            INSERT INTO expenses (
                description,
                amount,
                category,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                expense.description,
                expense.amount,
                expense.category,
                expense.created_at.isoformat()
            )
        )

        expense.id = cursor.lastrowid

        connection.commit()
        connection.close()

        return expense

    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            ORDER BY id
            """
        ).fetchall()

        connection.close()

        return self._convert_rows_to_expenses(rows)

    def update(self, expense):
        connection = get_connection()

        cursor = connection.execute(
            """
            UPDATE expenses
            SET description = ?,
                amount = ?,
                category = ?
            WHERE id = ?
            """,
            (
                expense.description,
                expense.amount,
                expense.category,
                expense.id
            )
        )

        connection.commit()
        connection.close()

        return cursor.rowcount > 0

    def delete(self, expense_id):
        connection = get_connection()

        cursor = connection.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        connection.commit()
        connection.close()

        return cursor.rowcount > 0

    def get_by_date(self, date):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            WHERE DATE(created_at) = ?
            ORDER BY id
            """,
            (date,)
        ).fetchall()

        connection.close()

        return self._convert_rows_to_expenses(rows)

    def search_by_description(self, keyword):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            WHERE description LIKE ?
            ORDER BY created_at DESC
            """,
            (f"%{keyword}%",)
        ).fetchall()

        connection.close()

        return self._convert_rows_to_expenses(rows)

    def filter_by_category(self, category):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            ORDER BY created_at DESC
            """,
            (category,)
        ).fetchall()

        connection.close()

        return self._convert_rows_to_expenses(rows)

    def filter_by_amount_range(self, minimum, maximum):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            WHERE amount BETWEEN ? AND ?
            ORDER BY amount ASC
            """,
            (minimum, maximum)
        ).fetchall()

        connection.close()

        return self._convert_rows_to_expenses(rows)

    def _convert_rows_to_expenses(self, rows):
        expenses = []

        for row in rows:
            expense = Expense(
                row["id"],
                row["description"],
                row["amount"],
                row["category"],
                datetime.fromisoformat(row["created_at"])
            )

            expenses.append(expense)

        return expenses