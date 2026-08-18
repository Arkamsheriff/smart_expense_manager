from datetime import datetime, timedelta


class ReportService:

    def __init__(self, expense_manager):
        self.expense_manager = expense_manager

    def today(self):
        today = datetime.now().strftime("%Y-%m-%d")

        return self.expense_manager.expenses_by_date(today)

    def total_for_expenses(self, expenses):
        total = 0

        for expense in expenses:
            total += expense.amount

        return total