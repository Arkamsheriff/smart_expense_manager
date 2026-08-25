from app.recurring.recurring_expense import RecurringExpense


def test_recurring_expense_creation():
    expense = RecurringExpense(
        1,
        "Netflix",
        649,
        "Entertainment",
        "Monthly",
        "2026-08"
    )

    assert expense.id == 1
    assert expense.description == "Netflix"
    assert expense.amount == 649
    assert expense.category == "Entertainment"
    assert expense.frequency == "Monthly"
    assert expense.start_date == "2026-08"
    assert expense.end_date is None
    assert expense.active is True


def test_recurring_expense_with_end_date():
    expense = RecurringExpense(
        2,
        "Insurance",
        2500,
        "Insurance",
        "Monthly",
        "2026-08",
        "2027-08"
    )

    assert expense.id == 2
    assert expense.description == "Insurance"
    assert expense.amount == 2500
    assert expense.category == "Insurance"
    assert expense.frequency == "Monthly"
    assert expense.start_date == "2026-08"
    assert expense.end_date == "2027-08"
    assert expense.active is True


def test_recurring_expense_inactive():
    expense = RecurringExpense(
        3,
        "Gym Membership",
        1500,
        "Health",
        "Monthly",
        "2026-08",
        active=False
    )

    assert expense.active is False


def test_recurring_expense_zero_amount():
    expense = RecurringExpense(
        4,
        "Free Subscription",
        0,
        "Subscription",
        "Monthly",
        "2026-08"
    )

    assert expense.amount == 0