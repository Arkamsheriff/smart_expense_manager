from datetime import datetime

import pytest

from app.income.income import Income
from app.income.income_repository import IncomeRepository


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


@pytest.fixture
def repository(tmp_path, monkeypatch):
    database = tmp_path / "income_test.db"

    # Never connect to production Supabase during tests.
    monkeypatch.setenv(
        "USE_POSTGRES",
        "false"
    )

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database)
    )

    repo = IncomeRepository()
    repo.initialize_table()

    return repo


def test_add_income(repository):
    income = Income(
        None,
        "Salary",
        50000,
        "Salary"
    )

    result = repository.add(
        income,
        TEST_USER_ID
    )

    assert result.id is not None
    assert result.description == "Salary"
    assert result.amount == 50000.0
    assert result.category == "Salary"


def test_get_by_id(repository):
    income = Income(
        None,
        "Freelance",
        15000,
        "Freelance"
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    result = repository.get_by_id(
        income.id,
        TEST_USER_ID
    )

    assert result is not None
    assert result.id == income.id
    assert result.description == "Freelance"
    assert result.amount == 15000.0


def test_get_missing_income(repository):
    result = repository.get_by_id(
        999,
        TEST_USER_ID
    )

    assert result is None


def test_get_all(repository):
    repository.add(
        Income(
            None,
            "Salary",
            50000,
            "Salary"
        ),
        TEST_USER_ID
    )

    repository.add(
        Income(
            None,
            "Freelance",
            15000,
            "Freelance"
        ),
        TEST_USER_ID
    )

    incomes = repository.get_all(
        TEST_USER_ID
    )

    assert len(incomes) == 2
    assert incomes[0].description == "Salary"
    assert incomes[1].description == "Freelance"


def test_update_income(repository):
    income = Income(
        None,
        "Salary",
        50000,
        "Salary"
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    income.description = "Updated Salary"
    income.amount = 55000
    income.category = "Job"

    result = repository.update(
        income,
        TEST_USER_ID
    )

    assert result is True

    updated = repository.get_by_id(
        income.id,
        TEST_USER_ID
    )

    assert updated.description == "Updated Salary"
    assert updated.amount == 55000.0
    assert updated.category == "Job"


def test_update_missing_income(repository):
    income = Income(
        999,
        "Unknown",
        1000,
        "Other"
    )

    result = repository.update(
        income,
        TEST_USER_ID
    )

    assert result is False


def test_delete_income(repository):
    income = Income(
        None,
        "Bonus",
        10000,
        "Bonus"
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    result = repository.delete(
        income.id,
        TEST_USER_ID
    )

    assert result is True

    assert repository.get_by_id(
        income.id,
        TEST_USER_ID
    ) is None


def test_delete_missing_income(repository):
    result = repository.delete(
        999,
        TEST_USER_ID
    )

    assert result is False


def test_total_income(repository):
    repository.add(
        Income(
            None,
            "Salary",
            50000,
            "Salary"
        ),
        TEST_USER_ID
    )

    repository.add(
        Income(
            None,
            "Freelance",
            15000,
            "Freelance"
        ),
        TEST_USER_ID
    )

    assert repository.total(
        TEST_USER_ID
    ) == 65000.0


def test_total_income_empty(repository):
    assert repository.total(
        TEST_USER_ID
    ) == 0


def test_get_by_category(repository):
    repository.add(
        Income(
            None,
            "Salary",
            50000,
            "Salary"
        ),
        TEST_USER_ID
    )

    repository.add(
        Income(
            None,
            "Freelance",
            15000,
            "Freelance"
        ),
        TEST_USER_ID
    )

    repository.add(
        Income(
            None,
            "Bonus",
            10000,
            "salary"
        ),
        TEST_USER_ID
    )

    incomes = repository.get_by_category(
        "SALARY",
        TEST_USER_ID
    )

    assert len(incomes) == 2

    assert all(
        income.category.lower() == "salary"
        for income in incomes
    )


def test_get_by_category_no_results(repository):
    repository.add(
        Income(
            None,
            "Salary",
            50000,
            "Salary"
        ),
        TEST_USER_ID
    )

    incomes = repository.get_by_category(
        "Investment",
        TEST_USER_ID
    )

    assert incomes == []


def test_created_at_is_preserved(repository):
    created_at = datetime(
        2026,
        8,
        25,
        10,
        30
    )

    income = Income(
        None,
        "Salary",
        50000,
        "Salary",
        created_at
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    result = repository.get_by_id(
        income.id,
        TEST_USER_ID
    )

    assert result.created_at == created_at


def test_income_user_isolation(repository):
    repository.add(
        Income(
            None,
            "User One Salary",
            50000,
            "Salary"
        ),
        TEST_USER_ID
    )

    repository.add(
        Income(
            None,
            "User Two Salary",
            60000,
            "Salary"
        ),
        OTHER_USER_ID
    )

    user_one_incomes = repository.get_all(
        TEST_USER_ID
    )

    user_two_incomes = repository.get_all(
        OTHER_USER_ID
    )

    assert len(user_one_incomes) == 1
    assert user_one_incomes[0].description == (
        "User One Salary"
    )

    assert len(user_two_incomes) == 1
    assert user_two_incomes[0].description == (
        "User Two Salary"
    )


def test_income_cannot_be_updated_by_other_user(
    repository
):
    income = Income(
        None,
        "Private Salary",
        50000,
        "Salary"
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    income.description = "Hacked Salary"
    income.amount = 999999

    result = repository.update(
        income,
        OTHER_USER_ID
    )

    assert result is False

    original = repository.get_by_id(
        income.id,
        TEST_USER_ID
    )

    assert original.description == "Private Salary"
    assert original.amount == 50000.0


def test_income_cannot_be_deleted_by_other_user(
    repository
):
    income = Income(
        None,
        "Private Salary",
        50000,
        "Salary"
    )

    repository.add(
        income,
        TEST_USER_ID
    )

    result = repository.delete(
        income.id,
        OTHER_USER_ID
    )

    assert result is False

    original = repository.get_by_id(
        income.id,
        TEST_USER_ID
    )

    assert original is not None
    assert original.description == "Private Salary"
