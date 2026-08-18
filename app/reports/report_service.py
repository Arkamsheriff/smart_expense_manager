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

    def this_week(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())

        expenses = self.expense_manager.list_expenses()

        return [
            expense
            for expense in expenses
            if start_of_week.date() <= expense.created_at.date() <= today.date()
        ]

    def this_month(self):
        today = datetime.now()

        expenses = self.expense_manager.list_expenses()

        return [
            expense
            for expense in expenses
            if (
                expense.created_at.year == today.year
                and expense.created_at.month == today.month
            )
        ]
    def category_summary(self, expenses):
        summary = {}

        for expense in expenses:
            if expense.category not in summary:
                summary[expense.category] = 0

            summary[expense.category] += expense.amount

        return summary
    def spending_statistics(self, expenses):
        if not expenses:
            return {
                "count": 0,
                "total": 0.0,
                "average": 0.0,
                "highest": 0.0,
                "lowest": 0.0
            }

        amounts = [expense.amount for expense in expenses]

        return {
            "count": len(amounts),
            "total": sum(amounts),
            "average": sum(amounts) / len(amounts),
            "highest": max(amounts),
            "lowest": min(amounts)
        }