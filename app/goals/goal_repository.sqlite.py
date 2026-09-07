from app.database.connection import get_connection
from app.goals.goal import Goal


class GoalRepository:

    def __init__(self):
        self.create_table()

    def create_table(self):
        connection = get_connection()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL NOT NULL DEFAULT 0,
                target_date TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()
        connection.close()

    def add(self, goal):
        connection = get_connection()

        cursor = connection.execute(
            """
            INSERT INTO goals
            (
                name,
                target_amount,
                current_amount,
                target_date,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                goal.name,
                goal.target_amount,
                goal.current_amount,
                goal.target_date,
                goal.created_at.isoformat()
            )
        )

        connection.commit()

        goal.id = cursor.lastrowid

        connection.close()

        return goal

    def get_by_id(self, goal_id):
        connection = get_connection()

        row = connection.execute(
            """
            SELECT
                id,
                name,
                target_amount,
                current_amount,
                target_date,
                created_at
            FROM goals
            WHERE id = ?
            """,
            (goal_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Goal(
            goal_id=row[0],
            name=row[1],
            target_amount=row[2],
            current_amount=row[3],
            target_date=row[4]
        )

    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT
                id,
                name,
                target_amount,
                current_amount,
                target_date,
                created_at
            FROM goals
            ORDER BY id
            """
        ).fetchall()

        connection.close()

        return [
            Goal(
                goal_id=row[0],
                name=row[1],
                target_amount=row[2],
                current_amount=row[3],
                target_date=row[4]
            )
            for row in rows
        ]

    def update(self, goal):
        connection = get_connection()

        cursor = connection.execute(
            """
            UPDATE goals
            SET
                name = ?,
                target_amount = ?,
                current_amount = ?,
                target_date = ?
            WHERE id = ?
            """,
            (
                goal.name,
                goal.target_amount,
                goal.current_amount,
                goal.target_date,
                goal.id
            )
        )

        connection.commit()

        updated = cursor.rowcount > 0

        connection.close()

        return updated

    def delete(self, goal_id):
        connection = get_connection()

        cursor = connection.execute(
            """
            DELETE FROM goals
            WHERE id = ?
            """,
            (goal_id,)
        )

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted