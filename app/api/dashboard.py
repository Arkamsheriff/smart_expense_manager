from collections import defaultdict

from fastapi import APIRouter

from app.api.auth import CurrentUser
from app.expense_manager import ExpenseManager
from app.income.income_manager import IncomeManager
from app.budget.budget_manager import BudgetManager
from app.goals.goal_manager import GoalManager
from app.recurring.recurring_manager import RecurringExpenseManager


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(current_user: CurrentUser):
    user_id = current_user["id"]

    expense_manager = ExpenseManager()
    income_manager = IncomeManager()
    budget_manager = BudgetManager()
    goal_manager = GoalManager()
    recurring_manager = RecurringExpenseManager()

    # ---------------------------------------------------------
    # Expenses and Income
    # ---------------------------------------------------------

    expenses = expense_manager.list_expenses(user_id)
    incomes = income_manager.get_all_income(user_id)

    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(i.amount for i in incomes)

    current_balance = total_income - total_expenses

    savings_rate = (
        (current_balance / total_income) * 100
        if total_income > 0
        else 0
    )

    # ---------------------------------------------------------
    # Recent Expenses
    # ---------------------------------------------------------

    recent_expenses = sorted(
        expenses,
        key=lambda e: e.created_at,
        reverse=True
    )[:5]

    # ---------------------------------------------------------
    # Recent Income
    # ---------------------------------------------------------

    recent_income = sorted(
        incomes,
        key=lambda i: i.created_at,
        reverse=True
    )[:5]

    # ---------------------------------------------------------
    # Expense by Category
    # ---------------------------------------------------------

    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.category] += expense.amount

    expense_by_category = [
        {
            "category": category,
            "total": total
        }
        for category, total in category_totals.items()
    ]

    # ---------------------------------------------------------
    # Income vs Expenses by Month
    # ---------------------------------------------------------

    monthly_data = defaultdict(
        lambda: {
            "income": 0.0,
            "expenses": 0.0
        }
    )

    for expense in expenses:
        month = expense.created_at.strftime("%Y-%m")
        monthly_data[month]["expenses"] += expense.amount

    for income in incomes:
        month = income.created_at.strftime("%Y-%m")
        monthly_data[month]["income"] += income.amount

    income_vs_expense_by_month = [
        {
            "month": month,
            "income": values["income"],
            "expenses": values["expenses"]
        }
        for month, values in sorted(monthly_data.items())
    ]

    # ---------------------------------------------------------
    # Budgets
    # ---------------------------------------------------------

    budgets = budget_manager.get_all_budgets(user_id)

    dashboard_budgets = []

    for budget in budgets:
        # Budget.month is currently used as the category field
        budget_category = budget.month

        category_expenses = [
            expense
            for expense in expenses
            if expense.category.lower() == budget_category.lower()
        ]

        spent = sum(
            expense.amount
            for expense in category_expenses
        )

        percent_used = (
            (spent / budget.amount) * 100
            if budget.amount > 0
            else 0
        )

        dashboard_budgets.append(
            {
                "id": budget.id,
                "category": budget_category,
                "amount": budget.amount,
                "period": "monthly",
                "spent": spent,
                "remaining": budget.amount - spent,
                "percentUsed": percent_used
            }
        )

    # ---------------------------------------------------------
    # Goals
    # ---------------------------------------------------------

    goals = goal_manager.get_all_goals(user_id)

    dashboard_goals = []

    for goal in goals:

        if goal.target_amount > 0:
            percent_complete = (
                goal.current_amount /
                goal.target_amount
            ) * 100
        else:
            percent_complete = 0

        percent_complete = min(
            percent_complete,
            100
        )

        remaining = max(
            goal.target_amount -
            goal.current_amount,
            0
        )

        dashboard_goals.append(
            {
                "id": goal.id,
                "name": goal.name,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "target_date": (
                    goal.target_date.isoformat()
                    if hasattr(goal.target_date, "isoformat")
                    else goal.target_date
                ),
                "remaining": remaining,
                "percentComplete": percent_complete
            }
        )

    # ---------------------------------------------------------
    # Upcoming Recurring Expenses
    # ---------------------------------------------------------

    recurring_expenses = (
        recurring_manager.get_all_recurring_expenses(user_id)
    )

    upcoming_recurring = []

    for recurring in recurring_expenses:

        if not recurring.active:
            continue

        next_due_date = recurring_manager.get_next_due_date(
            user_id,
            recurring.id
        )

        upcoming_recurring.append(
            {
                "id": recurring.id,
                "description": recurring.description,
                "amount": recurring.amount,
                "category": recurring.category,
                "frequency": recurring.frequency,
                "start_date": recurring.start_date,
                "end_date": recurring.end_date,
                "is_active": recurring.active,
                "next_due_date": next_due_date
            }
        )

    upcoming_recurring = sorted(
        upcoming_recurring,
        key=lambda recurring: recurring["next_due_date"] or ""
    )[:5]

    # ---------------------------------------------------------
    # Final Dashboard Response
    # ---------------------------------------------------------

    return {
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "currentBalance": current_balance,
        "savingsRate": savings_rate,

        "recentExpenses": [
            {
                "id": expense.id,
                "description": expense.description,
                "amount": expense.amount,
                "category": expense.category,
                "created_at": expense.created_at.isoformat()
            }
            for expense in recent_expenses
        ],

        "recentIncome": [
            {
                "id": income.id,
                "source": income.description,
                "amount": income.amount,
                "category": income.category,
                "received_at": income.created_at.isoformat()
            }
            for income in recent_income
        ],

        "upcomingRecurring": upcoming_recurring,

        "goals": dashboard_goals,

        "budgets": dashboard_budgets,

        "expenseByCategory": expense_by_category,

        "incomeVsExpenseByMonth": income_vs_expense_by_month
    }