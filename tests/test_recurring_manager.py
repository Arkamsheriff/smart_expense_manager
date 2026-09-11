import pytest

from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_manager import RecurringExpenseManager


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


class FakeRepository:
    def __init__(self):
        self.expenses = {}
        self.next_id = 1

    def add(self, expense, user_id=TEST_USER_ID):
        expense.id = self.next_id
        self.expenses[expense.id] = (expense, user_id)
        self.next_id += 1
        return expense

    def get(self, expense_id, user_id=TEST_USER_ID):
        record = self.expenses.get(expense_id)

        if record is None:
            return None

        expense, owner_id = record

        if owner_id != user_id:
            return None

        return expense

    def get_all(self, user_id=TEST_USER_ID):
        return [
            expense
            for expense, owner_id in self.expenses.values()
            if owner_id == user_id
        ]

    def update(self, expense, user_id=TEST_USER_ID):
        record = self.expenses.get(expense.id)

        if record is None:
            return False

        _, owner_id = record

        if owner_id != user_id:
            return False

        self.expenses[expense.id] = (expense, user_id)
        return True

    def delete(self, expense_id, user_id=TEST_USER_ID):
        record = self.expenses.get(expense_id)

        if record is None:
            return False

        _, owner_id = record

        if owner_id != user_id:
            return False

        del self.expenses[expense_id]
        return True


def create_manager(user_id=TEST_USER_ID):
    return RecurringExpenseManager(
        FakeRepository(),
        user_id=user_id,
    )


def test_create_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
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
        "2027-08-25",
    )

    assert expense.end_date == "2027-08-25"


def test_create_inactive_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
        active=False,
    )

    assert expense.active is False


def test_get_recurring_expense():
    manager = create_manager()

    created = manager.create_recurring_expense(
        "Internet",
        999,
        "Utilities",
        "Monthly",
        "2026-08-25",
    )

    result = manager.get_recurring_expense(created.id)

    assert result is not None
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
        "2026-08-25",
    )

    manager.create_recurring_expense(
        "Internet",
        999,
        "Utilities",
        "Monthly",
        "2026-08-25",
    )

    expenses = manager.get_all_recurring_expenses()

    assert len(expenses) == 2


def test_get_all_only_returns_current_user():
    repository = FakeRepository()

    manager = RecurringExpenseManager(
        repository,
        user_id=TEST_USER_ID,
    )

    manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    other_manager = RecurringExpenseManager(
        repository,
        user_id=OTHER_USER_ID,
    )

    other_manager.create_recurring_expense(
        "Spotify",
        199,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    expenses = manager.get_all_recurring_expenses()

    assert len(expenses) == 1
    assert expenses[0].description == "Netflix"


def test_user_cannot_get_other_users_expense():
    repository = FakeRepository()

    manager = RecurringExpenseManager(
        repository,
        user_id=TEST_USER_ID,
    )

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    other_manager = RecurringExpenseManager(
        repository,
        user_id=OTHER_USER_ID,
    )

    assert other_manager.get_recurring_expense(expense.id) is None


def test_update_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    result = manager.update_recurring_expense(
        expense.id,
        "Netflix Premium",
        799,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    assert result is True

    updated = manager.get_recurring_expense(expense.id)

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
        "2026-08-25",
    )

    assert result is False


def test_other_user_cannot_update_expense():
    repository = FakeRepository()

    manager = RecurringExpenseManager(
        repository,
        user_id=TEST_USER_ID,
    )

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    other_manager = RecurringExpenseManager(
        repository,
        user_id=OTHER_USER_ID,
    )

    result = other_manager.update_recurring_expense(
        expense.id,
        "Hacked",
        1,
        "Misc",
        "Monthly",
        "2026-08-25",
    )

    assert result is False

    original = manager.get_recurring_expense(expense.id)

    assert original.description == "Netflix"
    assert original.amount == 649


def test_delete_recurring_expense():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    assert manager.delete_recurring_expense(expense.id) is True

    assert manager.get_recurring_expense(expense.id) is None


def test_delete_missing_expense():
    manager = create_manager()

    assert manager.delete_recurring_expense(99) is False


def test_other_user_cannot_delete_expense():
    repository = FakeRepository()

    manager = RecurringExpenseManager(
        repository,
        user_id=TEST_USER_ID,
    )

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    other_manager = RecurringExpenseManager(
        repository,
        user_id=OTHER_USER_ID,
    )

    assert other_manager.delete_recurring_expense(expense.id) is False

    assert manager.get_recurring_expense(expense.id) is not None


def test_set_active():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    assert manager.set_active(expense.id, False) is True

    assert manager.get_recurring_expense(expense.id).active is False


def test_set_active_missing():
    manager = create_manager()

    assert manager.set_active(99, False) is False


def test_toggle_active():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
    )

    assert expense.active is True

    assert manager.toggle_active(expense.id) is True

    assert manager.get_recurring_expense(expense.id).active is False

    assert manager.toggle_active(expense.id) is True

    assert manager.get_recurring_expense(expense.id).active is True


def test_toggle_active_missing():
    manager = create_manager()

    assert manager.toggle_active(99) is False


def test_goal_next_due_monthly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2026-08-25",
    )

    assert manager.get_next_due_date(expense.id) == "2026-09-25"


def test_next_due_weekly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Subscription",
        100,
        "Entertainment",
        "Weekly",
        "2026-08-25",
    )

    assert manager.get_next_due_date(expense.id) == "2026-09-01"


def test_next_due_daily():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Daily Service",
        100,
        "Services",
        "Daily",
        "2026-08-25",
    )

    assert manager.get_next_due_date(expense.id) == "2026-08-26"


def test_next_due_yearly():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Insurance",
        5000,
        "Insurance",
        "Yearly",
        "2026-08-25",
    )

    assert manager.get_next_due_date(expense.id) == "2027-08-25"


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
        active=False,
    )

    assert manager.get_next_due_date(expense.id) is None


def test_monthly_next_due_handles_end_of_month():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Rent",
        15000,
        "Housing",
        "Monthly",
        "2026-01-31",
    )

    assert manager.get_next_due_date(expense.id) == "2026-02-28"


def test_leap_year_next_due():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Insurance",
        5000,
        "Insurance",
        "Yearly",
        "2024-02-29",
    )

    assert manager.get_next_due_date(expense.id) == "2025-02-28"


@pytest.mark.parametrize(
    "frequency",
    ["Daily", "Weekly", "Monthly", "Yearly"],
)
def test_valid_frequencies(frequency):
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Test",
        100,
        "Misc",
        frequency,
        "2026-08-25",
    )

    assert expense.frequency == frequency


def test_invalid_frequency():
    manager = create_manager()

    with pytest.raises(ValueError, match="Invalid frequency"):
        manager.create_recurring_expense(
            "Netflix",
            649,
            "Entertainment",
            "Invalid",
            "2026-08-25",
        )


def test_empty_description():
    manager = create_manager()

    with pytest.raises(ValueError, match="Description cannot be empty"):
        manager.create_recurring_expense(
            "   ",
            649,
            "Entertainment",
            "Monthly",
            "2026-08-25",
        )


def test_non_string_description():
    manager = create_manager()

    with pytest.raises(ValueError, match="Description must be text"):
        manager.create_recurring_expense(
            123,
            649,
            "Entertainment",
            "Monthly",
            "2026-08-25",
        )


def test_negative_amount():
    manager = create_manager()

    with pytest.raises(ValueError, match="Amount cannot be negative"):
        manager.create_recurring_expense(
            "Netflix",
            -1,
            "Entertainment",
            "Monthly",
            "2026-08-25",
        )


def test_invalid_amount():
    manager = create_manager()

    with pytest.raises(ValueError, match="Amount must be a number"):
        manager.create_recurring_expense(
            "Netflix",
            "abc",
            "Entertainment",
            "Monthly",
            "2026-08-25",
        )


def test_empty_category():
    manager = create_manager()

    with pytest.raises(ValueError, match="Category cannot be empty"):
        manager.create_recurring_expense(
            "Netflix",
            649,
            "   ",
            "Monthly",
            "2026-08-25",
        )


def test_non_string_category():
    manager = create_manager()

    with pytest.raises(ValueError, match="Category must be text"):
        manager.create_recurring_expense(
            "Netflix",
            649,
            123,
            "Monthly",
            "2026-08-25",
        )


def test_invalid_date():
    manager = create_manager()

    with pytest.raises(ValueError, match="Date must use YYYY-MM-DD format"):
        manager.create_recurring_expense(
            "Netflix",
            649,
            "Entertainment",
            "Monthly",
            "2026-08",
        )


def test_invalid_end_date():
    manager = create_manager()

    with pytest.raises(ValueError, match="Date must use YYYY-MM-DD format"):
        manager.create_recurring_expense(
            "Netflix",
            649,
            "Entertainment",
            "Monthly",
            "2026-08-25",
            "2027-08",
        )


def test_end_date_before_start_date():
    manager = create_manager()

    with pytest.raises(
        ValueError,
        match="End date cannot be before start date",
    ):
        manager.create_recurring_expense(
            "Netflix",
            649,
            "Entertainment",
            "Monthly",
            "2026-08-25",
            "2026-08-24",
        )


def test_description_and_category_are_trimmed():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "  Netflix  ",
        649,
        "  Entertainment  ",
        "Monthly",
        "2026-08-25",
    )

    assert expense.description == "Netflix"
    assert expense.category == "Entertainment"


def test_create_with_explicit_user_id():
    manager = create_manager()

    expense = manager.create_recurring_expense(
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08-25",
        user_id=OTHER_USER_ID,
    )

    assert manager.get_recurring_expense(
        expense.id,
        user_id=OTHER_USER_ID,
    ) is not None

    assert manager.get_recurring_expense(
        expense.id,
        user_id=TEST_USER_ID,
    ) is None