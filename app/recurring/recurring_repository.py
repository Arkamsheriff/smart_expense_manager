from app.database.connection import get_connection
from app.recurring.recurring_expense import RecurringExpense


class RecurringExpenseRepository:

    def __init__(self):
        self._initialize_table()

    def _initialize_table(self):
        connection = get_connection()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS recurring_expenses (
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

        connection.commit()
        connection.close()

    def add(self, recurring_expense):
        connection = get_connection()

        cursor = connection.execute(
            """
            INSERT INTO recurring_expenses (
                description,
                amount,
                category,
                frequency,
                start_date,
                end_date,
                active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recurring_expense.description,
                recurring_expense.amount,
                recurring_expense.category,
                recurring_expense.frequency,
                recurring_expense.start_date,
                recurring_expense.end_date,
                int(recurring_expense.active)
            )
        )

        connection.commit()

        recurring_expense.id = cursor.lastrowid

        connection.close()

        return recurring_expense

    def get(self, recurring_expense_id):
        connection = get_connection()

        row = connection.execute(
            """
            SELECT
                id,
                description,
                amount,
                category,
                frequency,
                start_date,
                end_date,
                active
            FROM recurring_expenses
            WHERE id = ?
            """,
            (recurring_expense_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return self._row_to_expense(row)

    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT
                id,
                description,
                amount,
                category,
                frequency,
                start_date,
                end_date,
                active
            FROM recurring_expenses
            ORDER BY id
            """
        ).fetchall()

        connection.close()

        return [
            self._row_to_expense(row)
            for row in rows
        ]

    def update(self, recurring_expense):
        connection = get_connection()

        cursor = connection.execute(
            """
            UPDATE recurring_expenses
            SET
                description = ?,
                amount = ?,
                category = ?,
                frequency = ?,
                start_date = ?,
                end_date = ?,
                active = ?
            WHERE id = ?
            """,
            (
                recurring_expense.description,
                recurring_expense.amount,
                recurring_expense.category,
                recurring_expense.frequency,
                recurring_expense.start_date,
                recurring_expense.end_date,
                int(recurring_expense.active),
                recurring_expense.id
            )
        )

        connection.commit()

        updated = cursor.rowcount > 0

        connection.close()

        return updated

    def delete(self, recurring_expense_id):
        connection = get_connection()

        cursor = connection.execute(
            """
            DELETE FROM recurring_expenses
            WHERE id = ?
            """,
            (recurring_expense_id,)
        )

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted

    def _row_to_expense(self, row):
        return RecurringExpense(
            row["id"],
            row["description"],
            row["amount"],
            row["category"],
            row["frequency"],
            row["start_date"],
            row["end_date"],
            bool(row["active"])
        )