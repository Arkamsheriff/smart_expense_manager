from app.database.repository import (
    initialize_database,
    ExpenseRepository
)
from app.expense import Expense


def test_repository_add_and_get_all(tmp_path, monkeypatch):

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(expense)

    expenses = repository.get_all()

    assert len(expenses) == 1
    assert expenses[0].description == "Rent"
    assert expenses[0].amount == 500.00
    assert expenses[0].category == "Housing"


def test_repository_delete(tmp_path, monkeypatch):

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Food",
        200.00,
        "Food"
    )

    repository.add(expense)

    result = repository.delete(expense.id)

    assert result is True
    assert repository.get_all() == []

def test_repository_update(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(expense)

    expense.description = "House Rent"
    expense.amount = 550.00
    expense.category = "Housing"

    result = repository.update(expense)

    assert result is True

    expenses = repository.get_all()

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "House Rent"
    assert expenses[0].amount == 550.00
    assert expenses[0].category == "Housing"

def test_repository_get_by_date(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(expense)

    date = expense.created_at.strftime("%Y-%m-%d")

    expenses = repository.get_by_date(date)

    assert len(expenses) == 1
    assert expenses[0].description == "Rent"