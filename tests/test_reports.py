from app.expense_manager import ExpenseManager
from app.reports.report_service import ReportService


def test_today_report(tmp_path, monkeypatch):
    manager = ExpenseManager()

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.repository import initialize_database

    initialize_database()

    manager = ExpenseManager()

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    report = ReportService(manager)

    expenses = report.today()

    assert len(expenses) == 1
    assert expenses[0].id == expense.id


def test_report_total():
    class FakeExpense:
        def __init__(self, amount):
            self.amount = amount

    expenses = [
        FakeExpense(100.00),
        FakeExpense(200.00),
        FakeExpense(50.00)
    ]

    report = ReportService(None)

    assert report.total_for_expenses(expenses) == 350.00

def test_this_week(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.repository import initialize_database

    initialize_database()

    manager = ExpenseManager()

    expense = manager.add_expense(
        "Food",
        200.00,
        "Food"
    )

    report = ReportService(manager)

    expenses = report.this_week()

    assert len(expenses) == 1
    assert expenses[0].id == expense.id


def test_this_month(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.repository import initialize_database

    initialize_database()

    manager = ExpenseManager()

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    report = ReportService(manager)

    expenses = report.this_month()

    assert len(expenses) == 1
    assert expenses[0].id == expense.id

def test_category_summary():
    class FakeExpense:
        def __init__(self, category, amount):
            self.category = category
            self.amount = amount

    expenses = [
        FakeExpense("Food", 200.00),
        FakeExpense("Food", 150.75),
        FakeExpense("Housing", 500.00),
        FakeExpense("Transport", 100.00)
    ]

    report = ReportService(None)

    summary = report.category_summary(expenses)

    assert summary["Food"] == 350.75
    assert summary["Housing"] == 500.00
    assert summary["Transport"] == 100.00

def test_spending_statistics():
    class FakeExpense:
        def __init__(self, amount):
            self.amount = amount

    expenses = [
        FakeExpense(100.00),
        FakeExpense(200.00),
        FakeExpense(50.00),
        FakeExpense(150.00)
    ]

    report = ReportService(None)

    statistics = report.spending_statistics(expenses)

    assert statistics["count"] == 4
    assert statistics["total"] == 500.00
    assert statistics["average"] == 125.00
    assert statistics["highest"] == 200.00
    assert statistics["lowest"] == 50.00

def test_spending_statistics_empty():
    service = ReportService(None)

    result = service.spending_statistics([])

    assert result == {
        "count": 0,
        "total": 0.0,
        "average": 0.0,
        "highest": 0.0,
        "lowest": 0.0
    }