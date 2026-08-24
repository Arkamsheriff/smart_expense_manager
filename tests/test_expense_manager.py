from app.expense_manager import ExpenseManager


def create_manager(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    from app.database.repository import initialize_database

    initialize_database()

    return ExpenseManager()


def test_add_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    assert expense.id == 1
    assert expense.description == "Rent"
    assert expense.amount == 500.00
    assert expense.category == "Housing"


def test_expense_id_increments(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

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


def test_total_expenses(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Food",
        150.75,
        "Food"
    )

    assert manager.total_expenses() == 650.75


def test_category_total(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Groceries",
        150.75,
        "Food"
    )

    manager.add_expense(
        "Restaurant",
        100.00,
        "Food"
    )

    assert manager.category_total("Food") == 250.75


def test_delete_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Food",
        150.00,
        "Food"
    )

    result = manager.delete_expense(1)

    assert result is True

    expenses = manager.list_expenses()

    assert len(expenses) == 1
    assert expenses[0].id == 2


def test_delete_nonexistent_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    result = manager.delete_expense(99)

    assert result is False

    expenses = manager.list_expenses()

    assert len(expenses) == 1

def test_update_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    result = manager.update_expense(
        expense.id,
        "House Rent",
        550.00,
        "Housing"
    )

    assert result is True

    expenses = manager.list_expenses()

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "House Rent"
    assert expenses[0].amount == 550.00
    assert expenses[0].category == "Housing"

def test_update_nonexistent_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.update_expense(
        99,
        "Something",
        100.00,
        "Misc"
    )

    assert result is False

def test_expenses_by_date(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    date = expense.created_at.strftime("%Y-%m-%d")

    expenses = manager.expenses_by_date(date)

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "Rent"

def test_search_expenses(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Monthly Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Restaurant Dinner",
        200.00,
        "Food"
    )

    results = manager.search_expenses("Rent")

    assert len(results) == 1
    assert results[0].description == "Monthly Rent"


def test_filter_expenses_by_category(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Monthly Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Groceries",
        150.00,
        "Food"
    )

    manager.add_expense(
        "Restaurant",
        200.00,
        "Food"
    )

    results = manager.filter_expenses_by_category("Food")

    assert len(results) == 2

    for expense in results:
        assert expense.category == "Food"


def test_filter_expenses_by_amount(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        "Food",
        150.00,
        "Food"
    )

    manager.add_expense(
        "Shopping",
        300.00,
        "Shopping"
    )

    results = manager.filter_expenses_by_amount(200.00, 500.00)

    assert len(results) == 2

    for expense in results:
        assert 200.00 <= expense.amount <= 500.00

def test_category_total_case_insensitive(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        "Groceries",
        150.75,
        "Food"
    )

    manager.add_expense(
        "Restaurant",
        100.00,
        "Food"
    )

    manager.add_expense(
        "Rent",
        500.00,
        "Housing"
    )

    assert manager.category_total("food") == 250.75
    assert manager.category_total("FOOD") == 250.75