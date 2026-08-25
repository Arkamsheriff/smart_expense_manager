from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_manager import RecurringExpenseManager


class FakeRepository:

    def __init__(self):
        self.expenses = {}
        self.next_id = 1

    def add(self, expense):
        expense.id = self.next_id
        self.expenses[expense.id] = expense
        self.next_id += 1
        return expense

    def get(self, expense_id):
        return self.expenses.get(expense_id)

    def get_all(self):
        return list(self.expenses.values())

    def update(self, expense):
        if expense.id not in self.expenses:
            return False

        self.expenses[expense.id] = expense
        return True

    def delete(self, expense_id):
        if expense_id not in self.expenses:
            return False

        del self.expenses[expense_id]
        return True


def create_manager():
    return RecurringExpenseManager(
        FakeRepository()
    )


def test_create_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    assert expense.id == 1
    assert expense.description == "Netflix"
    assert expense.amount == 649
    assert expense.frequency == "Monthly"


def test_create_with_end_date():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Insurance",
        2500,
        "Insurance",
        "Monthly",
        "2026-08-25",
        "2027-08-25"
    )

    assert expense.end_date == "2027-08-25"


def test_get_recurring_expense():
    manager = create_manager()

    created = manager.create_recurring_expense(
        "Internet",
        999,
        "Utilities",
        "Monthly",
        "2026-08-25"
    )

    result = manager.get_recurring_expense(
        created.id
    )

    assert result.description == "Internet"


def test_get_missing_expense():
    manager = create_manager()

    assert manager.get_recurring_expense(99) is None


def test_get_all_recurring_expenses():
    manager = create_manager()

    manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    manager.create_recurring_expense(
        "Internet",
        999,
        "Utilities",
        "Monthly",
        "2026-08-25"
    )

    expenses = manager.get_all_recurring_expenses()

    assert len(expenses) == 2


def test_update_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    result = manager.update_recurring_expense(
        expense.id,
        "Netflix Premium",
        799,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    assert result is True

    updated = manager.get_recurring_expense(
        expense.id
    )

    assert updated.description == "Netflix Premium"
    assert updated.amount == 799


def test_update_missing_expense():
    manager = create_manager()

    result = manager.update_recurring_expense(
        99,
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    assert result is False


def test_delete_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    assert manager.delete_recurring_expense(
        expense.id
    ) is True

    assert manager.get_recurring_expense(
        expense.id
    ) is None


def test_delete_missing_expense():
    manager = create_manager()

    assert manager.delete_recurring_expense(
        99
    ) is False


def test_set_active():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    assert manager.set_active(
        expense.id,
        False
    ) is True

    assert manager.get_recurring_expense(
        expense.id
    ).active is False


def test_toggle_active():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25"
    )

    manager.toggle_active(expense.id)

    assert manager.get_recurring_expense(
        expense.id
    ).active is False


def test_goal_next_due_monthly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2026-08-25"
    )

    assert manager.get_next_due_date(
        expense.id
    ) == "2026-09-25"


def test_next_due_weekly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Subscription",
        100,
        "Entertainment",
        "Weekly",
        "2026-08-25"
    )

    assert manager.get_next_due_date(
        expense.id
    ) == "2026-09-01"


def test_next_due_daily():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Daily Service",
        100,
        "Services",
        "Daily",
        "2026-08-25"
    )

    assert manager.get_next_due_date(
        expense.id
    ) == "2026-08-26"


def test_next_due_yearly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Insurance",
        5000,
        "Insurance",
        "Yearly",
        "2026-08-25"
    )

    assert manager.get_next_due_date(
        expense.id
    ) == "2027-08-25"


def test_next_due_missing():
    manager = create_manager()

    assert manager.get_next_due_date(99) is None


def test_next_due_inactive():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
        active=False
    )

    assert manager.get_next_due_date(
        expense.id
    ) is None