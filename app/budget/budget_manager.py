from app.budget.budget import Budget
from app.budget.budget_repository import BudgetRepository
from app.database.connection import DEFAULT_USER_ID


class BudgetManager:

    def __init__(self, repository=None, user_id=DEFAULT_USER_ID):
        self.repository = repository or BudgetRepository()
        self.user_id = user_id
        if hasattr(self.repository, "initialize_table"):
            self.repository.initialize_table()

    def set_budget(self, *args, user_id=None, **kwargs):
        if len(args) == 3:
            uid, month, amount = args
        elif len(args) == 2:
            month, amount = args
            uid = user_id or self.user_id
        elif "month" in kwargs and "amount" in kwargs:
            month = kwargs["month"]
            amount = kwargs["amount"]
            uid = user_id or kwargs.get("user_id", self.user_id)
        else:
            raise TypeError("set_budget requires month and amount")

        existing_budget = self.repository.get_by_month(month, uid)

        if existing_budget:
            existing_budget.amount = float(amount)
            self.repository.update(existing_budget, uid)
            return existing_budget

        budget = Budget(
            0,
            month,
            float(amount)
        )

        return self.repository.add(budget, uid)

    def get_budget(self, *args, user_id=None):
        if len(args) == 2:
            uid, month = args
        elif len(args) == 1:
            month = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("get_budget requires month")

        return self.repository.get_by_month(month, uid)

    def get_all_budgets(self, user_id=None):
        uid = user_id or self.user_id
        return self.repository.get_all(uid)

    def update_budget(self, *args, user_id=None, **kwargs):
        if len(args) == 4:
            uid, budget_id, month, amount = args
        elif len(args) == 3:
            budget_id, month, amount = args
            uid = user_id or self.user_id
        elif "budget_id" in kwargs and "month" in kwargs and "amount" in kwargs:
            budget_id = kwargs["budget_id"]
            month = kwargs["month"]
            amount = kwargs["amount"]
            uid = user_id or kwargs.get("user_id", self.user_id)
        else:
            raise TypeError("update_budget requires budget_id, month, and amount")

        budget = Budget(
            budget_id,
            month,
            float(amount)
        )

        return self.repository.update(budget, uid)

    def delete_budget(self, *args, user_id=None):
        if len(args) == 2:
            uid, budget_id = args
        elif len(args) == 1:
            budget_id = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("delete_budget requires budget_id")

        return self.repository.delete(budget_id, uid)

    def budget_remaining(self, *args, user_id=None):
        if len(args) == 3:
            uid, month, total_expenses = args
        elif len(args) == 2:
            month, total_expenses = args
            uid = user_id or self.user_id
        else:
            raise TypeError("budget_remaining requires month and total_expenses")

        budget = self.get_budget(month, user_id=uid)

        if budget is None:
            return None

        return budget.amount - total_expenses

    def budget_utilization(self, *args, user_id=None):
        if len(args) == 3:
            uid, month, total_expenses = args
        elif len(args) == 2:
            month, total_expenses = args
            uid = user_id or self.user_id
        else:
            raise TypeError("budget_utilization requires month and total_expenses")

        budget = self.get_budget(month, user_id=uid)

        if budget is None:
            return None

        if budget.amount == 0:
            return 0

        return (total_expenses / budget.amount) * 100

    def is_budget_exceeded(self, *args, user_id=None):
        if len(args) == 3:
            uid, month, total_expenses = args
        elif len(args) == 2:
            month, total_expenses = args
            uid = user_id or self.user_id
        else:
            raise TypeError("is_budget_exceeded requires month and total_expenses")

        budget = self.get_budget(month, user_id=uid)

        if budget is None:
            return False

        return total_expenses > budget.amount