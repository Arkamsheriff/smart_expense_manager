import sqlite3

import pytest

from app.database.repository import (
    initialize_database,
    ExpenseRepository
)
from app.expense import Expense


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


def setup_test_database(tmp_path, monkeypatch):
    """
    Configure an isolated SQLite database for repository tests.
    """

    database_path = tmp_path / "test.db"

    monkeypatch.setenv(
        "USE_POSTGRES",
        "false"
    )

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    initialize_database()

    return database_path


def test_repository_add_and_get_all(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    expenses = repository.get_all(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Rent"
    assert expenses[0].amount == 500.00
    assert expenses[0].category == "Housing"


def test_repository_delete(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Food",
        200.00,
        "Food"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    result = repository.delete(
        expense.id,
        TEST_USER_ID
    )

    assert result is True

    assert repository.get_all(
        TEST_USER_ID
    ) == []


def test_repository_update(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    expense.description = "House Rent"
    expense.amount = 550.00
    expense.category = "Housing"

    result = repository.update(
        expense,
        TEST_USER_ID
    )

    assert result is True

    expenses = repository.get_all(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "House Rent"
    assert expenses[0].amount == 550.00
    assert expenses[0].category == "Housing"


def test_repository_get_by_date(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    date = expense.created_at.strftime(
        "%Y-%m-%d"
    )

    expenses = repository.get_by_date(
        date,
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Rent"


def test_repository_search_by_description(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Monthly Rent",
            500.00,
            "Housing"
        ),
        TEST_USER_ID
    )

    repository.add(
        Expense(
            0,
            "Grocery Shopping",
            200.00,
            "Food"
        ),
        TEST_USER_ID
    )

    expenses = repository.search_by_description(
        "Rent",
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Monthly Rent"
    assert expenses[0].amount == 500.00


def test_repository_filter_by_category(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Rent",
            500.00,
            "Housing"
        ),
        TEST_USER_ID
    )

    repository.add(
        Expense(
            0,
            "Groceries",
            200.00,
            "Food"
        ),
        TEST_USER_ID
    )

    repository.add(
        Expense(
            0,
            "Electricity",
            150.00,
            "Housing"
        ),
        TEST_USER_ID
    )

    expenses = repository.filter_by_category(
        "housing",
        TEST_USER_ID
    )

    assert len(expenses) == 2

    assert all(
        expense.category.lower() == "housing"
        for expense in expenses
    )


def test_repository_filter_by_amount_range(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    repository.add(
        Expense(
            0,
            "Coffee",
            100.00,
            "Food"
        ),
        TEST_USER_ID
    )

    repository.add(
        Expense(
            0,
            "Groceries",
            500.00,
            "Food"
        ),
        TEST_USER_ID
    )

    repository.add(
        Expense(
            0,
            "Rent",
            1500.00,
            "Housing"
        ),
        TEST_USER_ID
    )

    expenses = repository.filter_by_amount_range(
        100,
        500,
        TEST_USER_ID
    )

    assert len(expenses) == 2

    amounts = [
        expense.amount
        for expense in expenses
    ]

    assert 100.00 in amounts
    assert 500.00 in amounts
    assert 1500.00 not in amounts


def test_repository_user_isolation(tmp_path, monkeypatch):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    user_one_expense = Expense(
        0,
        "User One Expense",
        100.00,
        "Food"
    )

    user_two_expense = Expense(
        0,
        "User Two Expense",
        200.00,
        "Travel"
    )

    repository.add(
        user_one_expense,
        TEST_USER_ID
    )

    repository.add(
        user_two_expense,
        OTHER_USER_ID
    )

    user_one_expenses = repository.get_all(
        TEST_USER_ID
    )

    user_two_expenses = repository.get_all(
        OTHER_USER_ID
    )

    assert len(user_one_expenses) == 1
    assert user_one_expenses[0].description == "User One Expense"

    assert len(user_two_expenses) == 1
    assert user_two_expenses[0].description == "User Two Expense"


def test_repository_user_cannot_delete_other_users_expense(
    tmp_path,
    monkeypatch
):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Private Expense",
        500.00,
        "Food"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    result = repository.delete(
        expense.id,
        OTHER_USER_ID
    )

    assert result is False

    expenses = repository.get_all(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Private Expense"


def test_repository_user_cannot_update_other_users_expense(
    tmp_path,
    monkeypatch
):

    setup_test_database(tmp_path, monkeypatch)

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Private Expense",
        500.00,
        "Food"
    )

    repository.add(
        expense,
        TEST_USER_ID
    )

    expense.description = "Hacked Expense"
    expense.amount = 9999.00

    result = repository.update(
        expense,
        OTHER_USER_ID
    )

    assert result is False

    expenses = repository.get_all(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Private Expense"
    assert expenses[0].amount == 500.00


def test_database_directory_created(tmp_path, monkeypatch):

    database_path = (
        tmp_path /
        "new_data" /
        "test.db"
    )

    monkeypatch.setenv(
        "USE_POSTGRES",
        "false"
    )

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.connection import get_connection

    connection = get_connection()

    assert database_path.parent.exists()
    assert database_path.exists()

    connection.close()


def test_repository_add_database_error(monkeypatch):

    class FailingConnection:

        def execute(self, *args, **kwargs):
            raise sqlite3.OperationalError(
                "database error"
            )

        def rollback(self):
            self.rollback_called = True

        def close(self):
            self.close_called = True

    connection = FailingConnection()

    monkeypatch.setattr(
        "app.database.repository.get_connection",
        lambda: connection
    )

    repository = ExpenseRepository()

    expense = Expense(
        0,
        "Rent",
        500.00,
        "Housing"
    )

    with pytest.raises(sqlite3.Error):
        repository.add(
            expense,
            TEST_USER_ID
        )

    assert connection.rollback_called is True
    assert connection.close_called is True


def test_repository_update_database_error(monkeypatch):

    class FailingConnection:

        def execute(self, *args, **kwargs):
            raise sqlite3.OperationalError(
                "database error"
            )

        def rollback(self):
            self.rollback_called = True

        def close(self):
            self.close_called = True

    connection = FailingConnection()

    monkeypatch.setattr(
        "app.database.repository.get_connection",
        lambda: connection
    )

    repository = ExpenseRepository()

    expense = Expense(
        1,
        "Rent",
        500.00,
        "Housing"
    )

    with pytest.raises(sqlite3.Error):
        repository.update(
            expense,
            TEST_USER_ID
        )

    assert connection.rollback_called is True
    assert connection.close_called is True


def test_repository_delete_database_error(monkeypatch):

    class FailingConnection:

        def execute(self, *args, **kwargs):
            raise sqlite3.OperationalError(
                "database error"
            )

        def rollback(self):
            self.rollback_called = True

        def close(self):
            self.close_called = True

    connection = FailingConnection()

    monkeypatch.setattr(
        "app.database.repository.get_connection",
        lambda: connection
    )

    repository = ExpenseRepository()

    with pytest.raises(sqlite3.Error):
        repository.delete(
            1,
            TEST_USER_ID
        )

    assert connection.rollback_called is True
    assert connection.close_called is True


def test_initialize_database_error(monkeypatch):

    class FailingConnection:

        def execute(self, *args, **kwargs):
            raise sqlite3.OperationalError(
                "database error"
            )

        def rollback(self):
            self.rollback_called = True

        def close(self):
            self.close_called = True

    connection = FailingConnection()

    monkeypatch.setattr(
        "app.database.repository.get_connection",
        lambda: connection
    )

    with pytest.raises(sqlite3.Error):
        initialize_database()

    assert connection.rollback_called is True
    assert connection.close_called is True
