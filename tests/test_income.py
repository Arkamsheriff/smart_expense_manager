from datetime import datetime

from app.income.income import Income


def test_income_creation():
    income = Income(
        1,
        "Salary",
        50000,
        "Salary"
    )

    assert income.id == 1
    assert income.description == "Salary"
    assert income.amount == 50000.0
    assert income.category == "Salary"
    assert isinstance(income.created_at, datetime)


def test_income_with_custom_date():
    created_at = datetime(
        2026,
        8,
        25,
        10,
        30
    )

    income = Income(
        2,
        "Freelance",
        15000,
        "Freelance",
        created_at
    )

    assert income.id == 2
    assert income.description == "Freelance"
    assert income.amount == 15000.0
    assert income.category == "Freelance"
    assert income.created_at == created_at


def test_income_amount_is_float():
    income = Income(
        3,
        "Bonus",
        10000,
        "Bonus"
    )

    assert isinstance(income.amount, float)
    assert income.amount == 10000.0


def test_income_repr():
    income = Income(
        4,
        "Salary",
        50000,
        "Salary"
    )

    result = repr(income)

    assert "Income(" in result
    assert "Salary" in result
    assert "50000.0" in result