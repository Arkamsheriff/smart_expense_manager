from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_cli import (
    display_recurring_menu,
    get_frequency,
    get_date,
    get_optional_date,
    display_recurring_expense,
    display_recurring_expenses,
    handle_recurring_menu,
)


class FakeRecurringManager:

    def __init__(self):
        self.expenses = {}
        self.next_id = 1

    def create_recurring_expense(
        self,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date=None
    ):
        expense = RecurringExpense(
            self.next_id,
            description,
            amount,
            category,
            frequency,
            start_date,
            end_date,
            True
        )

        self.expenses[expense.id] = expense
        self.next_id += 1

        return expense

    def get_recurring_expense(self, expense_id):
        return self.expenses.get(expense_id)

    def get_all_recurring_expenses(self):
        return list(self.expenses.values())

    def update_recurring_expense(
        self,
        expense_id,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date,
        active
    ):
        expense = self.expenses.get(expense_id)

        if expense is None:
            return False

        expense.description = description
        expense.amount = amount
        expense.category = category
        expense.frequency = frequency
        expense.start_date = start_date
        expense.end_date = end_date
        expense.active = active

        return True

    def delete_recurring_expense(self, expense_id):
        if expense_id not in self.expenses:
            return False

        del self.expenses[expense_id]
        return True

    def toggle_active(self, expense_id):
        expense = self.expenses.get(expense_id)

        if expense is None:
            return False

        expense.active = not expense.active

        return True

    def get_next_due_date(self, expense_id):
        expense = self.expenses.get(expense_id)

        if expense is None or not expense.active:
            return None

        return expense.start_date


def test_display_recurring_menu(capsys):
    display_recurring_menu()

    output = capsys.readouterr().out

    assert "RECURRING EXPENSES" in output
    assert "Create Recurring Expense" in output
    assert "View Recurring Expense" in output
    assert "View All Recurring Expenses" in output
    assert "Update Recurring Expense" in output
    assert "Delete Recurring Expense" in output
    assert "Activate/Deactivate" in output
    assert "Next Due Date" in output
    assert "Back" in output


def test_get_frequency_daily(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    assert get_frequency() == "Daily"


def test_get_frequency_weekly(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    assert get_frequency() == "Weekly"


def test_get_frequency_monthly(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "3"
    )

    assert get_frequency() == "Monthly"


def test_get_frequency_yearly(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "4"
    )

    assert get_frequency() == "Yearly"


def test_get_frequency_invalid_then_valid(monkeypatch):
    inputs = iter([
        "99",
        "2"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_frequency() == "Weekly"


def test_get_date_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2027-06-15"
    )

    assert get_date("Date: ") == "2027-06-15"


def test_get_date_invalid_then_valid(monkeypatch):
    inputs = iter([
        "2027-99-99",
        "invalid",
        "2027-12-25"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_date("Date: ") == "2027-12-25"


def test_get_optional_date_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2027-12-31"
    )

    assert get_optional_date("End date: ") == "2027-12-31"


def test_get_optional_date_blank(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: ""
    )

    assert get_optional_date("End date: ") is None


def test_get_optional_date_invalid_then_valid(monkeypatch):
    inputs = iter([
        "wrong",
        "2028-01-01"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_optional_date("End date: ") == "2028-01-01"


def test_display_recurring_expense(capsys):
    expense = RecurringExpense(
        1,
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2027-01-01",
        "2027-12-31",
        True
    )

    display_recurring_expense(expense)

    output = capsys.readouterr().out

    assert "Netflix" in output
    assert "649.00" in output
    assert "Entertainment" in output
    assert "Monthly" in output
    assert "2027-01-01" in output
    assert "2027-12-31" in output
    assert "Active" in output


def test_display_recurring_expense_no_end_date(capsys):
    expense = RecurringExpense(
        1,
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2027-01-01",
        None,
        True
    )

    display_recurring_expense(expense)

    output = capsys.readouterr().out

    assert "No end date" in output


def test_display_recurring_expense_inactive(capsys):
    expense = RecurringExpense(
        1,
        "Subscription",
        500,
        "Entertainment",
        "Monthly",
        "2027-01-01",
        None,
        False
    )

    display_recurring_expense(expense)

    output = capsys.readouterr().out

    assert "Inactive" in output


def test_display_recurring_expenses_empty(capsys):
    display_recurring_expenses([])

    output = capsys.readouterr().out

    assert "No recurring expenses found." in output


def test_display_recurring_expenses(capsys):
    expenses = [
        RecurringExpense(
            1,
            "Rent",
            15000,
            "Housing",
            "Monthly",
            "2027-01-01",
            None,
            True
        ),
        RecurringExpense(
            2,
            "Netflix",
            649,
            "Entertainment",
            "Monthly",
            "2027-01-01",
            None,
            False
        )
    ]

    display_recurring_expenses(expenses)

    output = capsys.readouterr().out

    assert "Rent" in output
    assert "15000.00" in output
    assert "Netflix" in output
    assert "649.00" in output
    assert "Active" in output
    assert "Inactive" in output


def test_handle_recurring_back(monkeypatch):
    manager = FakeRecurringManager()

    inputs = iter([
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)


def test_handle_recurring_invalid_choice(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "99",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Invalid choice." in output


def test_handle_recurring_create(monkeypatch):
    manager = FakeRecurringManager()

    inputs = iter([
        "1",
        "Netflix",
        "649",
        "Entertainment",
        "3",
        "2027-01-01",
        "",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    expense = manager.get_recurring_expense(1)

    assert expense.description == "Netflix"
    assert expense.amount == 649
    assert expense.category == "Entertainment"
    assert expense.frequency == "Monthly"
    assert expense.start_date == "2027-01-01"
    assert expense.end_date is None


def test_handle_recurring_create_with_end_date(monkeypatch):
    manager = FakeRecurringManager()

    inputs = iter([
        "1",
        "Insurance",
        "2500",
        "Insurance",
        "1",
        "2027-01-01",
        "2027-12-31",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    expense = manager.get_recurring_expense(1)

    assert expense.end_date == "2027-12-31"


def test_handle_recurring_view(monkeypatch, capsys):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "2",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Rent" in output
    assert "15000.00" in output
    assert "Housing" in output


def test_handle_recurring_view_missing(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "2",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Recurring expense not found." in output


def test_handle_recurring_view_all(monkeypatch, capsys):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2027-01-01"
    )

    manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "3",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Rent" in output
    assert "Netflix" in output


def test_handle_recurring_view_all_empty(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "3",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "No recurring expenses found." in output


def test_handle_recurring_update(monkeypatch):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Old Rent",
        10000,
        "Housing",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "4",
        "1",
        "New Rent",
        "12000",
        "Housing",
        "3",
        "2027-02-01",
        "2027-12-31",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    expense = manager.get_recurring_expense(1)

    assert expense.description == "New Rent"
    assert expense.amount == 12000
    assert expense.frequency == "Monthly"
    assert expense.start_date == "2027-02-01"
    assert expense.end_date == "2027-12-31"


def test_handle_recurring_update_missing(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "4",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Recurring expense not found." in output


def test_handle_recurring_delete(monkeypatch):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "5",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    assert manager.get_recurring_expense(1) is None


def test_handle_recurring_delete_missing(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "5",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Recurring expense not found." in output


def test_handle_recurring_toggle_active(monkeypatch):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "6",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    expense = manager.get_recurring_expense(1)

    assert expense.active is False


def test_handle_recurring_toggle_missing(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "6",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Recurring expense not found." in output


def test_handle_recurring_next_due(monkeypatch, capsys):
    manager = FakeRecurringManager()

    manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2027-01-01"
    )

    inputs = iter([
        "7",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Next due date: 2027-01-01" in output


def test_handle_recurring_next_due_missing(monkeypatch, capsys):
    manager = FakeRecurringManager()

    inputs = iter([
        "7",
        "999",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "Recurring expense not found." in output


def test_handle_recurring_next_due_unavailable(monkeypatch, capsys):
    manager = FakeRecurringManager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2027-01-01"
    )

    expense.active = False

    inputs = iter([
        "7",
        "1",
        "8"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_recurring_menu(manager)

    output = capsys.readouterr().out

    assert "No next due date available." in output