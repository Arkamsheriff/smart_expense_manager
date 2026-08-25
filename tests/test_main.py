from app import main as main_module
import matplotlib

matplotlib.use("Agg")


def test_main_exit(monkeypatch):
    inputs = iter([
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_add_expense(monkeypatch):
    inputs = iter([
        "1",
        "TestExpense",
        "100",
        "TestCategory",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_total_expenses(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "3",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_list_expenses(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Food",
        "200",
        "Food",
        "5",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_delete_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "2",
        "1",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_category_total(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Groceries",
        "150.75",
        "Food",
        "4",
        "Food",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_update_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "6",
        "1",
        "HouseRent",
        "550",
        "Housing",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_reports_menu(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "7",
        "1",
        "2",
        "3",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_monthly_reports(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Food",
        "200",
        "Food",
        "7",
        "4",
        "5",
        "6",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_charts(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Food",
        "200",
        "Food",
        "7",
        "7",
        "1",
        "3",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main(show_charts=False)


def test_main_pie_chart(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Food",
        "200",
        "Food",
        "7",
        "7",
        "2",
        "3",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main(show_charts=False)


def test_main_search_by_description(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Monthly Rent",
        "500",
        "Housing",
        "1",
        "Groceries",
        "200",
        "Food",
        "9",
        "1",
        "Rent",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_filter_by_category(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "1",
        "Groceries",
        "200",
        "Food",
        "9",
        "2",
        "Food",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_filter_by_amount(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "Rent",
        "500",
        "Housing",
        "1",
        "Groceries",
        "200",
        "Food",
        "9",
        "3",
        "200",
        "500",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_delete_nonexistent_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "2",
        "99",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_update_nonexistent_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "6",
        "99",
        "Something",
        "100",
        "Misc",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_invalid_choice(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "99",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_list_expenses_empty(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "5",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_empty_reports(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "7",
        "1",
        "3",
        "4",
        "5",
        "6",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_invalid_report_choice(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "7",
        "99",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_invalid_chart_choice(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "7",
        "7",
        "99",
        "3",
        "8",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main(show_charts=False)


def test_main_export(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    monkeypatch.chdir(tmp_path)

    inputs = iter([
        "1",
        "Food",
        "200",
        "Food",
        "8",
        "1",
        "2",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()

    assert (tmp_path / "reports" / "expenses.csv").exists()


def test_main_invalid_export_choice(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "8",
        "99",
        "2",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_search_no_results(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "9",
        "1",
        "SomethingThatDoesNotExist",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_filter_category_no_results(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "9",
        "2",
        "NonexistentCategory",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_filter_amount_no_results(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "9",
        "3",
        "500",
        "1000",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_invalid_amount_range(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "9",
        "3",
        "500",
        "100",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_invalid_search_choice(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "9",
        "99",
        "4",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_financial_goals_menu(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "11",
        "9",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_create_financial_goal(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "11",
        "1",
        "Emergency Fund",
        "100000",
        "10000",
        "2027-06",
        "9",
        "13"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()

def test_main_recurring_expenses_menu(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "12",   # Recurring Expenses
        "8",    # Back
        "13"    # Exit
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()


def test_main_create_recurring_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "12",              # Recurring Expenses
        "1",               # Create
        "Monthly Rent",    # Description
        "15000",           # Amount
        "Housing",         # Category
        "3",               # Monthly
        "2026-08-25",      # Start date
        "",                # No end date
        "8",               # Back
        "13"               # Exit
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()