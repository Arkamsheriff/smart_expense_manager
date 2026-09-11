from app.expense_manager import ExpenseManager


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


def create_manager(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    # Force repository tests to use isolated SQLite,
    # never the production Supabase database.
    monkeypatch.setenv(
        "USE_POSTGRES",
        "false"
    )

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
        TEST_USER_ID,
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
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    expense2 = manager.add_expense(
        TEST_USER_ID,
        "Food",
        200.00,
        "Food"
    )

    assert expense1.id == 1
    assert expense2.id == 2


def test_total_expenses(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Food",
        150.75,
        "Food"
    )

    assert manager.total_expenses(
        TEST_USER_ID
    ) == 650.75


def test_category_total(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Groceries",
        150.75,
        "Food"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Restaurant",
        100.00,
        "Food"
    )

    assert manager.category_total(
        TEST_USER_ID,
        "Food"
    ) == 250.75


def test_delete_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Food",
        150.00,
        "Food"
    )

    result = manager.delete_expense(
        TEST_USER_ID,
        1
    )

    assert result is True

    expenses = manager.list_expenses(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].id == 2


def test_delete_nonexistent_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    result = manager.delete_expense(
        TEST_USER_ID,
        99
    )

    assert result is False

    expenses = manager.list_expenses(
        TEST_USER_ID
    )

    assert len(expenses) == 1


def test_update_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    result = manager.update_expense(
        TEST_USER_ID,
        expense.id,
        "House Rent",
        550.00,
        "Housing"
    )

    assert result is True

    expenses = manager.list_expenses(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "House Rent"
    assert expenses[0].amount == 550.00
    assert expenses[0].category == "Housing"


def test_update_nonexistent_expense(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.update_expense(
        TEST_USER_ID,
        99,
        "Something",
        100.00,
        "Misc"
    )

    assert result is False


def test_expenses_by_date(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    date = expense.created_at.strftime(
        "%Y-%m-%d"
    )

    expenses = manager.expenses_by_date(
        TEST_USER_ID,
        date
    )

    assert len(expenses) == 1
    assert expenses[0].id == expense.id
    assert expenses[0].description == "Rent"


def test_search_expenses(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Monthly Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Restaurant Dinner",
        200.00,
        "Food"
    )

    results = manager.search_expenses(
        TEST_USER_ID,
        "Rent"
    )

    assert len(results) == 1
    assert results[0].description == "Monthly Rent"


def test_filter_expenses_by_category(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Monthly Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Groceries",
        150.00,
        "Food"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Restaurant",
        200.00,
        "Food"
    )

    results = manager.filter_expenses_by_category(
        TEST_USER_ID,
        "Food"
    )

    assert len(results) == 2

    for expense in results:
        assert expense.category == "Food"


def test_filter_expenses_by_amount(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Food",
        150.00,
        "Food"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Shopping",
        300.00,
        "Shopping"
    )

    results = manager.filter_expenses_by_amount(
        TEST_USER_ID,
        200.00,
        500.00
    )

    assert len(results) == 2

    for expense in results:
        assert 200.00 <= expense.amount <= 500.00


def test_category_total_case_insensitive(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "Groceries",
        150.75,
        "Food"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Restaurant",
        100.00,
        "Food"
    )

    manager.add_expense(
        TEST_USER_ID,
        "Rent",
        500.00,
        "Housing"
    )

    assert manager.category_total(
        TEST_USER_ID,
        "food"
    ) == 250.75

    assert manager.category_total(
        TEST_USER_ID,
        "FOOD"
    ) == 250.75


def test_manager_user_isolation(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    manager.add_expense(
        TEST_USER_ID,
        "User One Expense",
        100.00,
        "Food"
    )

    manager.add_expense(
        OTHER_USER_ID,
        "User Two Expense",
        200.00,
        "Travel"
    )

    user_one_expenses = manager.list_expenses(
        TEST_USER_ID
    )

    user_two_expenses = manager.list_expenses(
        OTHER_USER_ID
    )

    assert len(user_one_expenses) == 1
    assert user_one_expenses[0].description == "User One Expense"

    assert len(user_two_expenses) == 1
    assert user_two_expenses[0].description == "User Two Expense"


def test_manager_cannot_delete_other_users_expense(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        TEST_USER_ID,
        "Private Expense",
        500.00,
        "Food"
    )

    result = manager.delete_expense(
        OTHER_USER_ID,
        expense.id
    )

    assert result is False

    expenses = manager.list_expenses(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Private Expense"


def test_manager_cannot_update_other_users_expense(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    expense = manager.add_expense(
        TEST_USER_ID,
        "Private Expense",
        500.00,
        "Food"
    )

    result = manager.update_expense(
        OTHER_USER_ID,
        expense.id,
        "Hacked Expense",
        9999.00,
        "Other"
    )

    assert result is False

    expenses = manager.list_expenses(
        TEST_USER_ID
    )

    assert len(expenses) == 1
    assert expenses[0].description == "Private Expense"
    assert expenses[0].amount == 500.00
    assert expenses[0].category == "Food"
