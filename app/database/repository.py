from app.database.connection import get_connection
from app.expense import Expense


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


class ExpenseRepository:

    def add(self, expense):
        connection = get_connection()

        cursor = connection.execute(
            """
            INSERT INTO expenses (description, amount, category)
            VALUES (?, ?, ?)
            """,
            (
                expense.description,
                expense.amount,
                expense.category
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
            SELECT id, description, amount, category
            FROM expenses
            ORDER BY id
            """
        ).fetchall()

        connection.close()

        expenses = []

        for row in rows:
            expense = Expense(
                row["id"],
                row["description"],
                row["amount"],
                row["category"]
            )

            expenses.append(expense)

        return expenses

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