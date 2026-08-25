from datetime import datetime

from app.income.income import Income
from app.income.income_cli import (
    display_income_menu,
    display_income,
    display_incomes,
    handle_income_menu
)


class FakeIncomeManager:

    def __init__(self):
        self.incomes = {}
        self.next_id = 1

    def create_income(
        self,
        description,
        amount,
        category
    ):
        income = Income(
            self.next_id,
            description,
            amount,
            category
        )

        self.incomes[income.id] = income
        self.next_id += 1

        return income

    def get_income(self, income_id):
        return self.incomes.get(income_id)

    def get_all_income(self):
        return list(self.incomes.values())

    def update_income(
        self,
        income_id,
        description,
        amount,
        category
    ):
        income = self.incomes.get(income_id)

        if income is None:
            return False

        income.description = description
        income.amount = float(amount)
        income.category = category

        return True

    def delete_income(self, income_id):
        if income_id not in self.incomes:
            return False

        del self.incomes[income_id]

        return True

    def total_income(self):
        return sum(
            income.amount
            for income in self.incomes.values()
        )

    def get_income_by_category(self, category):
        return [
            income
            for income in self.incomes.values()
            if income.category.lower()
            == category.lower()
        ]


def test_display_income_menu(capsys):
    display_income_menu()

    output = capsys.readouterr().out

    assert "INCOME MANAGEMENT" in output
    assert "Add Income" in output
    assert "View Income" in output
    assert "View All Income" in output
    assert "Update Income" in output
    assert "Delete Income" in output
    assert "Total Income" in output
    assert "Income by Category" in output
    assert "Back" in output


def test_display_income(capsys):
    income = Income(
        1,
        "Salary",
        50000,
        "Salary",
        datetime(2026, 8, 25, 10, 30)
    )

    display_income(income)

    output = capsys.readouterr().out

    assert "Salary" in output
    assert "50000.00" in output
    assert "Salary" in output
    assert "2026-08-25 10:30:00" in output


def test_display_incomes_empty(capsys):
    display_incomes([])

    output = capsys.readouterr().out

    assert "No income found." in output


def test_display_incomes(capsys):
    incomes = [
        Income(
            1,
            "Salary",
            50000,
            "Salary"
        ),
        Income(
            2,
            "Freelance",
            15000,
            "Freelance"
        )
    ]

    display_incomes(incomes)

    output = capsys.readouterr().out

    assert "Salary" in output
    assert "50000.00" in output
    assert "Freelance" in output
    assert "15000.00" in output


def test_handle_income_back(monkeypatch):
    manager = FakeIncomeManager()

    inputs = iter([
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)


def test_handle_income_invalid_choice(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    inputs = iter([
        "99",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Invalid choice." in output


def test_handle_income_create(monkeypatch):
    manager = FakeIncomeManager()

    inputs = iter([
        "1",
        "Salary",
        "50000",
        "Salary",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    income = manager.get_income(1)

    assert income is not None
    assert income.description == "Salary"
    assert income.amount == 50000.0
    assert income.category == "Salary"


def test_handle_income_view(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    inputs = iter([
        "2",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Salary" in output
    assert "50000.00" in output


def test_handle_income_view_missing(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    inputs = iter([
        "2",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Income not found." in output


def test_handle_income_view_all(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Freelance",
        15000,
        "Freelance"
    )

    inputs = iter([
        "3",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Salary" in output
    assert "Freelance" in output


def test_handle_income_view_all_empty(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    inputs = iter([
        "3",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "No income found." in output


def test_handle_income_update(monkeypatch):
    manager = FakeIncomeManager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    inputs = iter([
        "4",
        "1",
        "Updated Salary",
        "55000",
        "Job",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    income = manager.get_income(1)

    assert income.description == "Updated Salary"
    assert income.amount == 55000.0
    assert income.category == "Job"


def test_handle_income_update_missing(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    inputs = iter([
        "4",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Income not found." in output


def test_handle_income_delete(monkeypatch):
    manager = FakeIncomeManager()

    manager.create_income(
        "Bonus",
        10000,
        "Bonus"
    )

    inputs = iter([
        "5",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    assert manager.get_income(1) is None


def test_handle_income_delete_missing(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    inputs = iter([
        "5",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Income not found." in output


def test_handle_income_total(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Freelance",
        15000,
        "Freelance"
    )

    inputs = iter([
        "6",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "65000.00" in output


def test_handle_income_category(
    monkeypatch,
    capsys
):
    manager = FakeIncomeManager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Bonus",
        10000,
        "Bonus"
    )

    inputs = iter([
        "7",
        "Salary",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_income_menu(manager)

    output = capsys.readouterr().out

    assert "Salary" in output
    assert "50000.00" in output
    assert "Bonus" not in output