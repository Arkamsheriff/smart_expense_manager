from datetime import datetime

from app.budget.budget import Budget
from app.budget.budget_cli import (
    display_budget_menu,
    get_month,
    get_budget_amount,
    display_budget_status,
    handle_budget_menu,
)


class FakeBudgetManager:

    def __init__(self):
        self.budgets = {}

    def set_budget(self, month, amount):
        budget = Budget(
            1,
            month,
            amount
        )

        self.budgets[month] = budget
        return budget

    def get_budget(self, month):
        return self.budgets.get(month)

    def get_all_budgets(self):
        return list(self.budgets.values())

    def delete_budget(self, budget_id):
        for month, budget in list(self.budgets.items()):
            if budget.id == budget_id:
                del self.budgets[month]
                return True

        return False

    def budget_remaining(self, month, total_expenses):
        budget = self.get_budget(month)

        if budget is None:
            return 0

        return budget.amount - total_expenses

    def budget_utilization(self, month, total_expenses):
        budget = self.get_budget(month)

        if budget is None or budget.amount == 0:
            return 0

        return (total_expenses / budget.amount) * 100


class FakeExpense:

    def __init__(self, amount, created_at):
        self.amount = amount
        self.created_at = created_at


class FakeExpenseManager:

    def __init__(self, expenses=None):
        self.expenses = expenses or []

    def list_expenses(self):
        return self.expenses


def test_display_budget_menu(capsys):
    display_budget_menu()

    output = capsys.readouterr().out

    assert "BUDGET MANAGEMENT" in output
    assert "1. Set Monthly Budget" in output
    assert "2. View Monthly Budget" in output
    assert "3. Budget Status" in output
    assert "4. View All Budgets" in output
    assert "5. Delete Budget" in output
    assert "6. Back" in output


def test_get_month_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2026-08"
    )

    assert get_month() == "2026-08"


def test_get_month_invalid_then_valid(monkeypatch, capsys):
    inputs = iter([
        "2026-13",
        "2026-08"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    result = get_month()

    assert result == "2026-08"

    output = capsys.readouterr().out

    assert "Invalid month" in output


def test_get_month_invalid_format_then_valid(monkeypatch, capsys):
    inputs = iter([
        "August",
        "2026/08",
        "2026-08"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    result = get_month()

    assert result == "2026-08"

    output = capsys.readouterr().out

    assert output.count("Invalid month") == 2


def test_get_budget_amount_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "5000"
    )

    assert get_budget_amount() == 5000.0


def test_get_budget_amount_zero(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "0"
    )

    assert get_budget_amount() == 0.0


def test_get_budget_amount_invalid_then_valid(monkeypatch, capsys):
    inputs = iter([
        "abc",
        "-500",
        "5000"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    result = get_budget_amount()

    assert result == 5000.0

    output = capsys.readouterr().out

    assert output.count("Invalid amount") == 2


def test_display_budget_status_within_budget(capsys):
    budget = Budget(
        1,
        "2026-08",
        5000
    )

    display_budget_status(
        budget,
        2000,
        3000,
        40
    )

    output = capsys.readouterr().out

    assert "BUDGET STATUS" in output
    assert "Month: 2026-08" in output
    assert "Budget: 5000.00" in output
    assert "Spent: 2000.00" in output
    assert "Remaining: 3000.00" in output
    assert "Utilization: 40.00%" in output
    assert "Status: Within Budget" in output


def test_display_budget_status_exceeded(capsys):
    budget = Budget(
        1,
        "2026-08",
        5000
    )

    display_budget_status(
        budget,
        6000,
        -1000,
        120
    )

    output = capsys.readouterr().out

    assert "Status: BUDGET EXCEEDED" in output


def test_handle_budget_set_budget(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "1",
        "2026-08",
        "5000",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    assert budget_manager.get_budget("2026-08") is not None
    assert budget_manager.get_budget("2026-08").amount == 5000

    output = capsys.readouterr().out

    assert "Budget for 2026-08 set successfully." in output


def test_handle_budget_view_budget(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    budget_manager.set_budget(
        "2026-08",
        5000
    )

    inputs = iter([
        "2",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "Month: 2026-08" in output
    assert "Monthly Budget: 5000.00" in output


def test_handle_budget_view_missing_budget(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "2",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "No budget found for this month." in output


def test_handle_budget_status(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager(
        [
            FakeExpense(
                1000,
                datetime(2026, 8, 10)
            ),
            FakeExpense(
                500,
                datetime(2026, 8, 15)
            ),
            FakeExpense(
                300,
                datetime(2026, 7, 15)
            )
        ]
    )

    budget_manager.set_budget(
        "2026-08",
        5000
    )

    inputs = iter([
        "3",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "Budget: 5000.00" in output
    assert "Spent: 1500.00" in output
    assert "Remaining: 3500.00" in output
    assert "Utilization: 30.00%" in output
    assert "Status: Within Budget" in output


def test_handle_budget_status_missing_budget(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "3",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "No budget found for this month." in output


def test_handle_budget_view_all_empty(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "4",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "No budgets found." in output


def test_handle_budget_view_all(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    budget_manager.set_budget(
        "2026-08",
        5000
    )

    budget_manager.set_budget(
        "2026-09",
        6000
    )

    inputs = iter([
        "4",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "All Budgets" in output
    assert "2026-08 5000.00" in output
    assert "2026-09 6000.00" in output


def test_handle_budget_delete(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    budget_manager.set_budget(
        "2026-08",
        5000
    )

    inputs = iter([
        "5",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    assert budget_manager.get_budget("2026-08") is None

    output = capsys.readouterr().out

    assert "Budget deleted successfully." in output


def test_handle_budget_delete_missing(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "5",
        "2026-08",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "No budget found for this month." in output


def test_handle_budget_invalid_choice(monkeypatch, capsys):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "99",
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )

    output = capsys.readouterr().out

    assert "Invalid choice." in output


def test_handle_budget_back(monkeypatch):
    budget_manager = FakeBudgetManager()
    expense_manager = FakeExpenseManager()

    inputs = iter([
        "6"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_budget_menu(
        budget_manager,
        expense_manager
    )