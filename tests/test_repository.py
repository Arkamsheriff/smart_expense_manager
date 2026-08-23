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

def test_repository_search_by_description(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Monthly Rent",
            500.00,
            "Housing"
        )
    )

    repository.add(
        Expense(
            0,
            "Grocery Shopping",
            200.00,
            "Food"
        )
    )

    expenses = repository.search_by_description("Rent")

    assert len(expenses) == 1
    assert expenses[0].description == "Monthly Rent"
    assert expenses[0].amount == 500.00

def test_repository_filter_by_category(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Rent",
            500.00,
            "Housing"
        )
    )

    repository.add(
        Expense(
            0,
            "Groceries",
            200.00,
            "Food"
        )
    )

    repository.add(
        Expense(
            0,
            "Electricity",
            150.00,
            "Housing"
        )
    )

    expenses = repository.filter_by_category("housing")

    assert len(expenses) == 2
    assert all(
        expense.category.lower() == "housing"
        for expense in expenses
    )

def test_repository_filter_by_amount_range(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Coffee",
            100.00,
            "Food"
        )
    )

    repository.add(
        Expense(
            0,
            "Groceries",
            500.00,
            "Food"
        )
    )

    repository.add(
        Expense(
            0,
            "Rent",
            1500.00,
            "Housing"
        )
    )

    expenses = repository.filter_by_amount_range(
        100,
        500
    )

    assert len(expenses) == 2

    amounts = [expense.amount for expense in expenses]

    assert 100.00 in amounts
    assert 500.00 in amounts
    assert 1500.00 not in amounts

def test_repository_filter_by_amount_range(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Coffee",
            100.00,
            "Food"
        )
    )

    repository.add(
        Expense(
            0,
            "Groceries",
            500.00,
            "Food"
        )
    )

    repository.add(
        Expense(
            0,
            "Rent",
            1500.00,
            "Housing"
        )
    )

    expenses = repository.filter_by_amount_range(100, 500)

    assert len(expenses) == 2

    amounts = [expense.amount for expense in expenses]

    assert 100.00 in amounts
    assert 500.00 in amounts
    assert 1500.00 not in amounts

def test_database_directory_created(tmp_path, monkeypatch):
    database_path = tmp_path / "new_data" / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.connection import get_connection

    connection = get_connection()

    assert database_path.parent.exists()
    assert database_path.exists()

    connection.close()