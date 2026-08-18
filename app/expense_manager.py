from app.expense import Expense


class ExpenseManager:

    def __init__(self):
        self.expenses = []
        self.next_id = 1

    def add_expense(self, description, amount, category):
        expense = Expense(
            self.next_id,
            description,
            amount,
            category
        )

        self.expenses.append(expense)
        self.next_id += 1

        return expense

    def list_expenses(self):
        return self.expenses

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                self.expenses.remove(expense)
                return True

        return False

    def total_expenses(self):
        total = 0

        for expense in self.expenses:
            total += expense.amount

        return total