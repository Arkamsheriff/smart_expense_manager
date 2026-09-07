from datetime import datetime, date

from app.database.connection import get_connection
from app.database.repository import ExpenseRepository
from app.expense import Expense

from app.income.income_repository import IncomeRepository
from app.income.income import Income

from app.budget.budget_repository import BudgetRepository
from app.budget.budget import Budget

from app.goals.goal_repository import GoalRepository
from app.goals.goal import Goal

from app.recurring.recurring_repository import RecurringExpenseRepository
from app.recurring.recurring_expense import RecurringExpense


MARKER = "POSTGRES_INTEGRATION_TEST"


def cleanup():
    """Remove all integration-test records."""
    connection = get_connection()

    try:
        for table in [
            "recurring_expenses",
            "goals",
            "budgets",
            "incomes",
            "expenses",
        ]:
            connection.execute(
                f"DELETE FROM {table} WHERE description LIKE %s"
                if table in ["expenses", "incomes", "recurring_expenses"]
                else (
                    f"DELETE FROM {table} WHERE name LIKE %s"
                    if table == "goals"
                    else f"DELETE FROM {table} WHERE month LIKE %s"
                ),
                (f"{MARKER}%",),
            )

        connection.commit()

    finally:
        connection.close()


def test_expenses():
    print("\n[1/5] Testing ExpenseRepository...")

    repository = ExpenseRepository()

    created_at = datetime.now()

    expense = Expense(
        None,
        f"{MARKER} Expense",
        500.0,
        "Food",
        created_at,
    )

    # CREATE
    result = repository.add(expense)

    assert result.id is not None
    print("  ✓ Add expense")

    # READ ALL
    expenses = repository.get_all()

    assert any(item.id == result.id for item in expenses)
    print("  ✓ Get all expenses")

    # READ BY DATE
    expenses_by_date = repository.get_by_date(created_at.date())

    assert any(item.id == result.id for item in expenses_by_date)
    print("  ✓ Get expense by date")

    # SEARCH
    search_results = repository.search_by_description(MARKER)

    assert any(item.id == result.id for item in search_results)
    print("  ✓ Search by description")

    # FILTER CATEGORY
    category_results = repository.filter_by_category("food")

    assert any(item.id == result.id for item in category_results)
    print("  ✓ Filter by category")

    # FILTER AMOUNT
    amount_results = repository.filter_by_amount_range(400, 600)

    assert any(item.id == result.id for item in amount_results)
    print("  ✓ Filter by amount range")

    # UPDATE
    result.description = f"{MARKER} Updated Expense"
    result.amount = 750.0
    result.category = "Transport"

    updated = repository.update(result)

    assert updated is True
    print("  ✓ Update expense")

    # VERIFY UPDATE
    updated_results = repository.search_by_description(
        f"{MARKER} Updated"
    )

    assert any(item.id == result.id for item in updated_results)
    print("  ✓ Verify update")

    # DELETE
    deleted = repository.delete(result.id)

    assert deleted is True
    print("  ✓ Delete expense")

    print("  ExpenseRepository PASSED")


def test_income():
    print("\n[2/5] Testing IncomeRepository...")

    repository = IncomeRepository()
    repository.initialize_table()

    created_at = datetime.now()

    income = Income(
        None,
        f"{MARKER} Income",
        50000.0,
        "Salary",
        created_at,
    )

    # CREATE
    result = repository.add(income)

    assert result.id is not None
    print("  ✓ Add income")

    # READ BY ID
    fetched = repository.get_by_id(result.id)

    assert fetched is not None
    assert fetched.id == result.id
    print("  ✓ Get income by ID")

    # READ ALL
    incomes = repository.get_all()

    assert any(item.id == result.id for item in incomes)
    print("  ✓ Get all incomes")

    # CATEGORY
    category_results = repository.get_by_category("salary")

    assert any(item.id == result.id for item in category_results)
    print("  ✓ Get income by category")

    # TOTAL
    total = repository.total()

    assert total >= 50000.0
    print("  ✓ Calculate total income")

    # UPDATE
    result.description = f"{MARKER} Updated Income"
    result.amount = 60000.0
    result.category = "Business"

    updated = repository.update(result)

    assert updated is True
    print("  ✓ Update income")

    # DELETE
    deleted = repository.delete(result.id)

    assert deleted is True
    print("  ✓ Delete income")

    print("  IncomeRepository PASSED")


def test_budget():
    print("\n[3/5] Testing BudgetRepository...")

    repository = BudgetRepository()
    repository.initialize_table()

    budget = Budget(
        None,
        f"{MARKER}_BUDGET",
        30000.0,
        datetime.now(),
    )

    # CREATE
    result = repository.add(budget)

    assert result.id is not None
    print("  ✓ Add budget")

    # READ BY MONTH
    fetched = repository.get_by_month(result.month)

    assert fetched is not None
    assert fetched.id == result.id
    print("  ✓ Get budget by month")

    # READ ALL
    budgets = repository.get_all()

    assert any(item.id == result.id for item in budgets)
    print("  ✓ Get all budgets")

    # UPDATE
    result.month = f"{MARKER}_UPDATED"
    result.amount = 40000.0

    updated = repository.update(result)

    assert updated is True
    print("  ✓ Update budget")

    # DELETE
    deleted = repository.delete(result.id)

    assert deleted is True
    print("  ✓ Delete budget")

    print("  BudgetRepository PASSED")


def test_goals():
    print("\n[4/5] Testing GoalRepository...")

    repository = GoalRepository()

    goal = Goal(
        None,
        f"{MARKER} Goal",
        100000.0,
        10000.0,
        date(2027, 12, 31),
    )

    # CREATE
    result = repository.add(goal)

    assert result.id is not None
    print("  ✓ Add goal")

    # READ BY ID
    fetched = repository.get_by_id(result.id)

    assert fetched is not None
    assert fetched.id == result.id
    print("  ✓ Get goal by ID")

    # READ ALL
    goals = repository.get_all()

    assert any(item.id == result.id for item in goals)
    print("  ✓ Get all goals")

    # UPDATE
    result.name = f"{MARKER} Updated Goal"
    result.target_amount = 150000.0
    result.current_amount = 25000.0
    result.target_date = "2028-12-31"

    updated = repository.update(result)

    assert updated is True
    print("  ✓ Update goal")

    # DELETE
    deleted = repository.delete(result.id)

    assert deleted is True
    print("  ✓ Delete goal")

    print("  GoalRepository PASSED")


def test_recurring_expenses():
    print("\n[5/5] Testing RecurringExpenseRepository...")

    repository = RecurringExpenseRepository()

    recurring = RecurringExpense(
        None,
        f"{MARKER} Recurring",
        2000.0,
        "Subscription",
        "monthly",
        date(2026, 9, 1),
        date(2027, 9, 1),
        True,
    )

    # CREATE
    result = repository.add(recurring)

    assert result.id is not None
    print("  ✓ Add recurring expense")

    # READ BY ID
    fetched = repository.get(result.id)

    assert fetched is not None
    assert fetched.id == result.id
    print("  ✓ Get recurring expense")

    # READ ALL
    recurring_expenses = repository.get_all()

    assert any(item.id == result.id for item in recurring_expenses)
    print("  ✓ Get all recurring expenses")

    # UPDATE
    result.description = f"{MARKER} Updated Recurring"
    result.amount = 2500.0
    result.category = "Entertainment"
    result.frequency = "yearly"
    result.start_date = date(2026, 10, 1)
    result.end_date = date(2028, 10, 1)
    result.active = False

    updated = repository.update(result)

    assert updated is True
    print("  ✓ Update recurring expense")

    # DELETE
    deleted = repository.delete(result.id)

    assert deleted is True
    print("  ✓ Delete recurring expense")

    print("  RecurringExpenseRepository PASSED")


def main():
    print("=" * 60)
    print("POSTGRESQL CRUD INTEGRATION TEST")
    print("=" * 60)

    print("\nCleaning old test data...")
    cleanup()

    try:
        test_expenses()
        test_income()
        test_budget()
        test_goals()
        test_recurring_expenses()

        print("\n" + "=" * 60)
        print("ALL POSTGRESQL CRUD TESTS PASSED")
        print("=" * 60)

    finally:
        print("\nCleaning test data...")
        cleanup()
        print("Cleanup completed.")


if __name__ == "__main__":
    main()