from datetime import datetime, timedelta
from io import StringIO
import csv
import sqlite3

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.database.connection import get_connection


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


def row_to_expense(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "description": row["description"],
        "amount": float(row["amount"]),
        "category": row["category"],
        "created_at": row["created_at"],
    }


def get_all_expenses() -> list[dict]:
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, description, amount, category, created_at
            FROM expenses
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [row_to_expense(row) for row in rows]

    finally:
        connection.close()


def parse_created_at(value: str) -> datetime:
    """
    Supports the common SQLite datetime formats used by the project.
    """
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return datetime.fromisoformat(value)


def period_report(start: datetime, end: datetime | None = None) -> dict:
    expenses = get_all_expenses()

    filtered = []

    for expense in expenses:
        created_at = parse_created_at(expense["created_at"])

        if created_at >= start and (end is None or created_at < end):
            filtered.append(expense)

    total = sum(expense["amount"] for expense in filtered)

    return {
        "expenses": filtered,
        "total": round(total, 2),
    }


@router.get("/today")
def today_report():
    now = datetime.now()

    start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    end = start + timedelta(days=1)

    return period_report(start, end)


@router.get("/weekly")
def weekly_report():
    now = datetime.now()

    start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Sunday-based week, matching the frontend's previous mock behaviour.
    days_since_sunday = (start.weekday() + 1) % 7

    start = start - timedelta(days=days_since_sunday)

    end = start + timedelta(days=7)

    return period_report(start, end)


@router.get("/monthly")
def monthly_report():
    now = datetime.now()

    start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    if start.month == 12:
        end = start.replace(
            year=start.year + 1,
            month=1,
        )
    else:
        end = start.replace(
            month=start.month + 1,
        )

    return period_report(start, end)


@router.get("/category-summary")
def category_summary():
    expenses = get_all_expenses()

    totals: dict[str, dict[str, float | int]] = {}

    for expense in expenses:
        category = expense["category"]

        if category not in totals:
            totals[category] = {
                "total": 0.0,
                "count": 0,
            }

        totals[category]["total"] += expense["amount"]
        totals[category]["count"] += 1

    overall_total = sum(
        expense["amount"]
        for expense in expenses
    )

    result = []

    for category, values in totals.items():
        category_total = float(values["total"])
        count = int(values["count"])

        percent = (
            (category_total / overall_total) * 100
            if overall_total > 0
            else 0
        )

        result.append(
            {
                "category": category,
                "total": round(category_total, 2),
                "count": count,
                "percentOfTotal": round(percent, 1),
            }
        )

    result.sort(
        key=lambda item: item["total"],
        reverse=True,
    )

    return result


@router.get("/statistics")
def spending_statistics():
    expenses = get_all_expenses()

    amounts = [
        expense["amount"]
        for expense in expenses
    ]

    if not amounts:
        return {
            "count": 0,
            "total": 0,
            "average": 0,
            "highest": 0,
            "lowest": 0,
        }

    total = sum(amounts)

    return {
        "count": len(amounts),
        "total": round(total, 2),
        "average": round(total / len(amounts), 2),
        "highest": round(max(amounts), 2),
        "lowest": round(min(amounts), 2),
    }


@router.get("/monthly-series")
def monthly_spending_series():
    expenses = get_all_expenses()

    now = datetime.now()

    months = []

    year = now.year
    month = now.month

    for _ in range(6):
        months.append(
            {
                "year": year,
                "month": month,
            }
        )

        month -= 1

        if month == 0:
            month = 12
            year -= 1

    months.reverse()

    result = []

    for month_info in months:
        year_value = month_info["year"]
        month_value = month_info["month"]

        total = 0.0

        for expense in expenses:
            created_at = parse_created_at(
                expense["created_at"]
            )

            if (
                created_at.year == year_value
                and created_at.month == month_value
            ):
                total += expense["amount"]

        month_label = datetime(
            year_value,
            month_value,
            1,
        ).strftime("%b")

        result.append(
            {
                "month": month_label,
                "total": round(total, 2),
            }
        )

    return result


@router.get("/export-csv")
def export_csv():
    expenses = get_all_expenses()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            "ID",
            "Description",
            "Amount",
            "Category",
            "Created At",
        ]
    )

    for expense in expenses:
        writer.writerow(
            [
                expense["id"],
                expense["description"],
                f'{expense["amount"]:.2f}',
                expense["category"],
                expense["created_at"],
            ]
        )

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                'attachment; filename="expenses.csv"'
            )
        },
    )