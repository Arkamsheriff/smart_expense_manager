from app.expense import Expense
from app.database.repository import ExpenseRepository


class ExpenseManager:

    def __init__(self):
        self.repository = ExpenseRepository()

    def add_expense(self, description, amount, category):
        expense = Expense(
            0,
            description,
            amount,
            category
        )

        return self.repository.add(expense)

    def list_expenses(self):
        return self.repository.get_all()

    def delete_expense(self, expense_id):
        return self.repository.delete(expense_id)

    def total_expenses(self):
        expenses = self.repository.get_all()

        total = 0

        for expense in expenses:
            total += expense.amount

        return total

    def category_total(self, category):
        expenses = self.repository.get_all()

        total = 0

        for expense in expenses:
            if expense.category == category:
                total += expense.amount

        return total

    def update_expense(self, expense_id, description, amount, category):
        expense = Expense(
            expense_id,
            description,
            amount,
            category
        )

        return self.repository.update(expense)