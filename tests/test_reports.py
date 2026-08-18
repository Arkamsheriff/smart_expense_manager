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