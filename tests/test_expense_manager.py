from app.expense_manager import ExpenseManager


def test_add_expense():
    manager = ExpenseManager()

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    assert expense.id == 1
    assert expense.description == "Rent"
    assert expense.amount == 500.00
    assert expense.category == "Housing"


def test_expense_id_increments():
    manager = ExpenseManager()

    expense1 = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    expense2 = manager.add_expense(
        "Food",
        200.00,
        "Food"
    )

    assert expense1.id == 1
    assert expense2.id == 2


def test_total_expenses():
    manager = ExpenseManager()

    manager.add_expense("Rent", 500.00, "Housing")
    manager.add_expense("Food", 150.75, "Food")

    assert manager.total_expenses() == 650.75


def test_category_total():
    manager = ExpenseManager()

    manager.add_expense("Rent", 500.00, "Housing")
    manager.add_expense("Groceries", 150.75, "Food")
    manager.add_expense("Restaurant", 100.00, "Food")

    assert manager.category_total("Food") == 250.75


def test_delete_expense():
    manager = ExpenseManager()

    manager.add_expense("Rent", 500.00, "Housing")
    manager.add_expense("Food", 150.00, "Food")

    result = manager.delete_expense(1)

    assert result is True
    assert len(manager.expenses) == 1
    assert manager.expenses[0].id == 2


def test_delete_nonexistent_expense():
    manager = ExpenseManager()

    manager.add_expense("Rent", 500.00, "Housing")

    result = manager.delete_expense(99)

    assert result is False
    assert len(manager.expenses) == 1