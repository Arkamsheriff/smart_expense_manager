from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_repository import RecurringExpenseRepository


def create_expense():
    return RecurringExpense(
        None,
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08"
    )


def test_repository_add_and_get(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    expense = repository.add(create_expense())

    assert expense.id is not None

    result = repository.get(expense.id)

    assert result is not None
    assert result.description == "Netflix"
    assert result.amount == 649
    assert result.category == "Entertainment"
    assert result.frequency == "Monthly"


def test_repository_get_missing(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    assert repository.get(999) is None


def test_repository_get_all(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    repository.add(create_expense())

    repository.add(
        RecurringExpense(
            None,
            "Internet",
            999,
            "Utilities",
            "Monthly",
            "2026-08"
        )
    )

    expenses = repository.get_all()

    assert len(expenses) == 2
    assert expenses[0].description == "Netflix"
    assert expenses[1].description == "Internet"


def test_repository_update(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    expense = repository.add(create_expense())

    expense.description = "Netflix Premium"
    expense.amount = 799

    assert repository.update(expense) is True

    result = repository.get(expense.id)

    assert result.description == "Netflix Premium"
    assert result.amount == 799


def test_repository_update_missing(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    expense = RecurringExpense(
        999,
        "Missing",
        100,
        "Misc",
        "Monthly",
        "2026-08"
    )

    assert repository.update(expense) is False


def test_repository_delete(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    expense = repository.add(create_expense())

    assert repository.delete(expense.id) is True
    assert repository.get(expense.id) is None


def test_repository_delete_missing(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repository = RecurringExpenseRepository()

    assert repository.delete(999) is False