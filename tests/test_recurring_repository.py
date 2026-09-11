import pytest

from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_repository import RecurringExpenseRepository


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


def create_expense(
    description="Netflix",
    amount=649,
    category="Entertainment",
    frequency="Monthly",
    start_date="2026-08-01",
    end_date=None,
    active=True,
):
    return RecurringExpense(
        None,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date,
        active,
    )


def setup_repository(tmp_path, monkeypatch):
    monkeypatch.setenv("USE_POSTGRES", "false")

    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database),
    )

    return RecurringExpenseRepository()


def test_repository_add_and_get(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    assert expense.id is not None

    result = repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    )

    assert result is not None
    assert result.description == "Netflix"
    assert result.amount == 649
    assert result.category == "Entertainment"
    assert result.frequency == "Monthly"
    assert result.start_date == "2026-08-01"
    assert result.active is True


def test_repository_add_with_end_date_and_inactive(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(
            description="Insurance",
            amount=2500,
            category="Insurance",
            frequency="Yearly",
            start_date="2026-08-01",
            end_date="2027-08-01",
            active=False,
        ),
        user_id=TEST_USER_ID,
    )

    result = repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    )

    assert result is not None
    assert result.end_date == "2027-08-01"
    assert result.active is False


def test_repository_get_missing(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    assert repository.get(
        999,
        user_id=TEST_USER_ID,
    ) is None


def test_repository_get_all(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    repository.add(
        create_expense(
            description="Internet",
            amount=999,
            category="Utilities",
        ),
        user_id=TEST_USER_ID,
    )

    expenses = repository.get_all(
        user_id=TEST_USER_ID,
    )

    assert len(expenses) == 2
    assert expenses[0].description == "Netflix"
    assert expenses[1].description == "Internet"


def test_repository_get_all_only_returns_current_user(
    tmp_path,
    monkeypatch,
):
    repository = setup_repository(tmp_path, monkeypatch)

    repository.add(
        create_expense("Netflix"),
        user_id=TEST_USER_ID,
    )

    repository.add(
        create_expense(
            description="Spotify",
            amount=199,
        ),
        user_id=OTHER_USER_ID,
    )

    expenses = repository.get_all(
        user_id=TEST_USER_ID,
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Netflix"


def test_repository_get_cannot_access_other_user(
    tmp_path,
    monkeypatch,
):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    assert repository.get(
        expense.id,
        user_id=OTHER_USER_ID,
    ) is None


def test_repository_update(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    expense.description = "Netflix Premium"
    expense.amount = 799
    expense.active = False

    assert repository.update(
        expense,
        user_id=TEST_USER_ID,
    ) is True

    result = repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    )

    assert result is not None
    assert result.description == "Netflix Premium"
    assert result.amount == 799
    assert result.active is False


def test_repository_update_missing(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = RecurringExpense(
        999,
        "Missing",
        100,
        "Misc",
        "Monthly",
        "2026-08-01",
    )

    assert repository.update(
        expense,
        user_id=TEST_USER_ID,
    ) is False


def test_repository_update_cannot_modify_other_user(
    tmp_path,
    monkeypatch,
):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    expense.description = "Hacked Netflix"
    expense.amount = 1

    assert repository.update(
        expense,
        user_id=OTHER_USER_ID,
    ) is False

    result = repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    )

    assert result is not None
    assert result.description == "Netflix"
    assert result.amount == 649


def test_repository_delete(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    assert repository.delete(
        expense.id,
        user_id=TEST_USER_ID,
    ) is True

    assert repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    ) is None


def test_repository_delete_missing(tmp_path, monkeypatch):
    repository = setup_repository(tmp_path, monkeypatch)

    assert repository.delete(
        999,
        user_id=TEST_USER_ID,
    ) is False


def test_repository_delete_cannot_delete_other_user(
    tmp_path,
    monkeypatch,
):
    repository = setup_repository(tmp_path, monkeypatch)

    expense = repository.add(
        create_expense(),
        user_id=TEST_USER_ID,
    )

    assert repository.delete(
        expense.id,
        user_id=OTHER_USER_ID,
    ) is False

    assert repository.get(
        expense.id,
        user_id=TEST_USER_ID,
    ) is not None