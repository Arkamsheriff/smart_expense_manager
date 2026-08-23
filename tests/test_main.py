from app import main as main_module
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

def test_main_exit(monkeypatch):
    inputs = iter([
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main()

def test_main_add_expense(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    inputs = iter([
        "1",
        "TestExpense",
        "100",
        "TestCategory",
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
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
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main_module.main(show_charts=False)