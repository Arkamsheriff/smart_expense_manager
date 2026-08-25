from datetime import datetime

import pytest

from app.database.connection import DATABASE_PATH
from app.income.income import Income
from app.income.income_repository import IncomeRepository


@pytest.fixture
def repository(tmp_path, monkeypatch):
    database = tmp_path / "income_test.db"

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

    result = repository.add(income)

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

    repository.add(income)

    result = repository.get_by_id(income.id)

    assert result is not None
    assert result.id == income.id
    assert result.description == "Freelance"
    assert result.amount == 15000.0


def test_get_missing_income(repository):
    result = repository.get_by_id(999)

    assert result is None


def test_get_all(repository):
    repository.add(
        Income(None, "Salary", 50000, "Salary")
    )

    repository.add(
        Income(None, "Freelance", 15000, "Freelance")
    )

    incomes = repository.get_all()

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

    repository.add(income)

    income.description = "Updated Salary"
    income.amount = 55000
    income.category = "Job"

    result = repository.update(income)

    assert result is True

    updated = repository.get_by_id(income.id)

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

    result = repository.update(income)

    assert result is False


def test_delete_income(repository):
    income = Income(
        None,
        "Bonus",
        10000,
        "Bonus"
    )

    repository.add(income)

    result = repository.delete(income.id)

    assert result is True
    assert repository.get_by_id(income.id) is None


def test_delete_missing_income(repository):
    result = repository.delete(999)

    assert result is False


def test_total_income(repository):
    repository.add(
        Income(None, "Salary", 50000, "Salary")
    )

    repository.add(
        Income(None, "Freelance", 15000, "Freelance")
    )

    assert repository.total() == 65000.0


def test_total_income_empty(repository):
    assert repository.total() == 0


def test_get_by_category(repository):
    repository.add(
        Income(None, "Salary", 50000, "Salary")
    )

    repository.add(
        Income(None, "Freelance", 15000, "Freelance")
    )

    repository.add(
        Income(None, "Bonus", 10000, "salary")
    )

    incomes = repository.get_by_category("SALARY")

    assert len(incomes) == 2
    assert all(
        income.category.lower() == "salary"
        for income in incomes
    )


def test_get_by_category_no_results(repository):
    repository.add(
        Income(None, "Salary", 50000, "Salary")
    )

    incomes = repository.get_by_category("Investment")

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

    repository.add(income)

    result = repository.get_by_id(income.id)

    assert result.created_at == created_at