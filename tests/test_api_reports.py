from datetime import datetime, timedelta

from app.api.reports import parse_created_at, row_to_expense


def add_expense(client, description, amount, category):
    response = client.post(
        "/api/expenses",
        json={
            "description": description,
            "amount": amount,
            "category": category,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_row_to_expense_with_datetime():
    created_at = datetime(2026, 9, 7, 10, 30, 0)

    row = {
        "id": 1,
        "description": "Lunch",
        "amount": 250,
        "category": "Food",
        "created_at": created_at,
    }

    result = row_to_expense(row)

    assert result["id"] == 1
    assert result["description"] == "Lunch"
    assert result["amount"] == 250.0
    assert result["category"] == "Food"
    assert result["created_at"] == "2026-09-07T10:30:00"


def test_parse_created_at_datetime():
    value = datetime(2026, 9, 7, 10, 30, 0)

    result = parse_created_at(value)

    assert result == value


def test_parse_created_at_string_formats():
    assert parse_created_at(
        "2026-09-07 10:30:00"
    ) == datetime(2026, 9, 7, 10, 30, 0)

    assert parse_created_at(
        "2026-09-07T10:30:00"
    ) == datetime(2026, 9, 7, 10, 30, 0)

    assert parse_created_at(
        "2026-09-07T10:30:00.123456"
    ) == datetime(2026, 9, 7, 10, 30, 0, 123456)


def test_parse_created_at_iso_timezone():
    result = parse_created_at(
        "2026-09-07T10:30:00+05:30"
    )

    assert result == datetime(2026, 9, 7, 10, 30, 0)


def test_today_report(client):
    add_expense(
        client,
        "Today Food",
        250,
        "Food",
    )

    response = client.get("/api/reports/today")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 250
    assert len(data["expenses"]) == 1
    assert data["expenses"][0]["description"] == "Today Food"


def test_weekly_report(client):
    add_expense(
        client,
        "Weekly Food",
        500,
        "Food",
    )

    response = client.get("/api/reports/weekly")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 500
    assert len(data["expenses"]) == 1


def test_monthly_report(client):
    add_expense(
        client,
        "Monthly Food",
        750,
        "Food",
    )

    response = client.get("/api/reports/monthly")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 750
    assert len(data["expenses"]) == 1


def test_category_summary(client):
    add_expense(
        client,
        "Lunch",
        250,
        "Food",
    )

    add_expense(
        client,
        "Dinner",
        750,
        "Food",
    )

    add_expense(
        client,
        "Taxi",
        500,
        "Transport",
    )

    response = client.get("/api/reports/category-summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["category"] == "Food"
    assert data[0]["total"] == 1000
    assert data[0]["count"] == 2
    assert data[0]["percentOfTotal"] == 66.7

    assert data[1]["category"] == "Transport"
    assert data[1]["total"] == 500
    assert data[1]["count"] == 1
    assert data[1]["percentOfTotal"] == 33.3


def test_category_summary_empty(client):
    response = client.get("/api/reports/category-summary")

    assert response.status_code == 200
    assert response.json() == []


def test_spending_statistics(client):
    add_expense(
        client,
        "Food",
        100,
        "Food",
    )

    add_expense(
        client,
        "Transport",
        300,
        "Transport",
    )

    add_expense(
        client,
        "Shopping",
        500,
        "Shopping",
    )

    response = client.get("/api/reports/statistics")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert data["total"] == 900
    assert data["average"] == 300
    assert data["highest"] == 500
    assert data["lowest"] == 100


def test_spending_statistics_empty(client):
    response = client.get("/api/reports/statistics")

    assert response.status_code == 200

    assert response.json() == {
        "count": 0,
        "total": 0,
        "average": 0,
        "highest": 0,
        "lowest": 0,
    }


def test_monthly_spending_series(client):
    add_expense(
        client,
        "Monthly Expense",
        1200,
        "Food",
    )

    response = client.get("/api/reports/monthly-series")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 6

    assert "month" in data[0]
    assert "total" in data[0]

    assert data[-1]["total"] == 1200


def test_export_csv_empty(client):
    response = client.get("/api/reports/export-csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "ID,Description,Amount,Category,Created At" in response.text


def test_export_csv_with_expenses(client):
    add_expense(
        client,
        "CSV Food",
        250,
        "Food",
    )

    add_expense(
        client,
        "CSV Taxi",
        150,
        "Transport",
    )

    response = client.get("/api/reports/export-csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    assert "ID,Description,Amount,Category,Created At" in response.text
    assert "CSV Food" in response.text
    assert "250.00" in response.text
    assert "CSV Taxi" in response.text
    assert "150.00" in response.text