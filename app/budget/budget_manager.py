from app.budget.budget import Budget
from app.budget.budget_repository import BudgetRepository


class BudgetManager:

    def __init__(self):
        self.repository = BudgetRepository()
        self.repository.initialize_table()

    def set_budget(self, month, amount):
        existing_budget = self.repository.get_by_month(month)

        if existing_budget:
            existing_budget.amount = amount
            self.repository.update(existing_budget)
            return existing_budget

        budget = Budget(
            0,
            month,
            amount
        )

        return self.repository.add(budget)

    def get_budget(self, month):
        return self.repository.get_by_month(month)

    def get_all_budgets(self):
        return self.repository.get_all()

    def update_budget(self, budget_id, month, amount):
        budget = Budget(
            budget_id,
            month,
            amount
        )

        return self.repository.update(budget)

    def delete_budget(self, budget_id):
        return self.repository.delete(budget_id)

    def budget_remaining(self, month, total_expenses):
        budget = self.get_budget(month)

        if budget is None:
            return None

        return budget.amount - total_expenses

    def budget_utilization(self, month, total_expenses):
        budget = self.get_budget(month)

        if budget is None:
            return None

        if budget.amount == 0:
            return 0

        return (total_expenses / budget.amount) * 100

    def is_budget_exceeded(self, month, total_expenses):
        budget = self.get_budget(month)

        if budget is None:
            return False

        return total_expenses > budget.amount