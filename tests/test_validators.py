from app.validators import (
    get_non_empty_input,
    get_positive_amount,
    get_valid_id
)


def test_get_non_empty_input(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Rent"
    )

    result = get_non_empty_input("Description: ")

    assert result == "Rent"


def test_get_positive_amount(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "500.50"
    )

    result = get_positive_amount("Amount: ")

    assert result == 500.50


def test_get_valid_id(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "10"
    )

    result = get_valid_id("ID: ")

    assert result == 10