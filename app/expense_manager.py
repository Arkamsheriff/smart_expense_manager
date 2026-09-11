from app.expense import Expense
from app.database.connection import DEFAULT_USER_ID
from app.database.repository import ExpenseRepository


class ExpenseManager:

    def __init__(self, repository=None, user_id=DEFAULT_USER_ID):
        self.repository = repository or ExpenseRepository()
        self.user_id = user_id

    def add_expense(self, *args, user_id=None, **kwargs):
        if len(args) == 4:
            uid, description, amount, category = args
        elif len(args) == 3:
            description, amount, category = args
            uid = user_id or self.user_id
        elif "description" in kwargs and "amount" in kwargs and "category" in kwargs:
            description = kwargs["description"]
            amount = kwargs["amount"]
            category = kwargs["category"]
            uid = user_id or kwargs.get("user_id", self.user_id)
        else:
            raise TypeError(
                "add_expense requires (description, amount, category) "
                "or (user_id, description, amount, category)"
            )

        expense = Expense(
            0,
            description,
            float(amount),
            category
        )

        return self.repository.add(expense, uid)

    def list_expenses(self, user_id=None):
        uid = user_id or self.user_id
        return self.repository.get_all(uid)

    def get_expense(self, expense_id, user_id=None):
        uid = user_id or self.user_id
        if hasattr(self.repository, "get_by_id"):
            return self.repository.get_by_id(expense_id, uid)
        for expense in self.list_expenses(uid):
            if expense.id == expense_id:
                return expense
        return None

    def delete_expense(self, *args, user_id=None):
        if len(args) == 2:
            uid, expense_id = args
        elif len(args) == 1:
            expense_id = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("delete_expense requires expense_id")

        return self.repository.delete(expense_id, uid)

    def total_expenses(self, user_id=None):
        uid = user_id or self.user_id
        expenses = self.repository.get_all(uid)

        total = 0.0

        for expense in expenses:
            total += expense.amount

        return total

    def category_total(self, *args, user_id=None):
        if len(args) == 2:
            uid, category = args
        elif len(args) == 1:
            category = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("category_total requires category")

        expenses = self.repository.get_all(uid)

        total = 0.0

        for expense in expenses:
            if expense.category.lower() == category.lower():
                total += expense.amount

        return total

    def update_expense(self, *args, user_id=None, **kwargs):
        if len(args) == 5:
            uid, expense_id, description, amount, category = args
        elif len(args) == 4:
            expense_id, description, amount, category = args
            uid = user_id or self.user_id
        elif "expense_id" in kwargs and "description" in kwargs and "amount" in kwargs and "category" in kwargs:
            expense_id = kwargs["expense_id"]
            description = kwargs["description"]
            amount = kwargs["amount"]
            category = kwargs["category"]
            uid = user_id or kwargs.get("user_id", self.user_id)
        else:
            raise TypeError(
                "update_expense requires (expense_id, description, amount, category)"
            )

        expense = Expense(
            expense_id,
            description,
            float(amount),
            category
        )

        return self.repository.update(expense, uid)

    def expenses_by_date(self, *args, user_id=None):
        if len(args) == 2:
            uid, date = args
        elif len(args) == 1:
            date = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("expenses_by_date requires date")

        return self.repository.get_by_date(date, uid)

    def search_expenses(self, *args, user_id=None):
        if len(args) == 2:
            uid, keyword = args
        elif len(args) == 1:
            keyword = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("search_expenses requires keyword")

        return self.repository.search_by_description(keyword, uid)

    def filter_expenses_by_category(self, *args, user_id=None):
        if len(args) == 2:
            uid, category = args
        elif len(args) == 1:
            category = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("filter_expenses_by_category requires category")

        return self.repository.filter_by_category(category, uid)

    def filter_expenses_by_amount(self, *args, user_id=None):
        if len(args) == 3:
            uid, minimum, maximum = args
        elif len(args) == 2:
            minimum, maximum = args
            uid = user_id or self.user_id
        else:
            raise TypeError("filter_expenses_by_amount requires minimum and maximum")

        return self.repository.filter_by_amount_range(minimum, maximum, uid)