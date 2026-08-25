from datetime import datetime

from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_repository import RecurringExpenseRepository


class RecurringExpenseManager:

    VALID_FREQUENCIES = {
        "Daily",
        "Weekly",
        "Monthly",
        "Yearly"
    }

    def __init__(self, repository=None):
        self.repository = (
            repository
            if repository is not None
            else RecurringExpenseRepository()
        )

    def create_recurring_expense(
        self,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date=None,
        active=True
    ):
        self._validate_description(description)
        self._validate_amount(amount)
        self._validate_category(category)
        self._validate_frequency(frequency)
        self._validate_date(start_date)

        if end_date is not None:
            self._validate_date(end_date)

            if end_date < start_date:
                raise ValueError(
                    "End date cannot be before start date."
                )

        expense = RecurringExpense(
            None,
            description.strip(),
            float(amount),
            category.strip(),
            frequency,
            start_date,
            end_date,
            active
        )

        return self.repository.add(expense)

    def get_recurring_expense(self, expense_id):
        return self.repository.get(expense_id)

    def get_all_recurring_expenses(self):
        return self.repository.get_all()

    def update_recurring_expense(
        self,
        expense_id,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date=None,
        active=True
    ):
        expense = self.repository.get(expense_id)

        if expense is None:
            return False

        self._validate_description(description)
        self._validate_amount(amount)
        self._validate_category(category)
        self._validate_frequency(frequency)
        self._validate_date(start_date)

        if end_date is not None:
            self._validate_date(end_date)

            if end_date < start_date:
                raise ValueError(
                    "End date cannot be before start date."
                )

        expense.description = description.strip()
        expense.amount = float(amount)
        expense.category = category.strip()
        expense.frequency = frequency
        expense.start_date = start_date
        expense.end_date = end_date
        expense.active = active

        return self.repository.update(expense)

    def delete_recurring_expense(self, expense_id):
        return self.repository.delete(expense_id)

    def set_active(self, expense_id, active):
        expense = self.repository.get(expense_id)

        if expense is None:
            return False

        expense.active = bool(active)

        return self.repository.update(expense)

    def toggle_active(self, expense_id):
        expense = self.repository.get(expense_id)

        if expense is None:
            return False

        expense.active = not expense.active

        return self.repository.update(expense)

    def get_next_due_date(self, expense_id):
        expense = self.repository.get(expense_id)

        if expense is None:
            return None

        if not expense.active:
            return None

        return self._calculate_next_date(
            expense.start_date,
            expense.frequency
        )

    def _calculate_next_date(self, start_date, frequency):
        date = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        if frequency == "Daily":
            from datetime import timedelta
            date += timedelta(days=1)

        elif frequency == "Weekly":
            from datetime import timedelta
            date += timedelta(weeks=1)

        elif frequency == "Monthly":
            month = date.month + 1
            year = date.year

            if month > 12:
                month = 1
                year += 1

            day = min(
                date.day,
                self._days_in_month(year, month)
            )

            date = date.replace(
                year=year,
                month=month,
                day=day
            )

        elif frequency == "Yearly":
            try:
                date = date.replace(
                    year=date.year + 1
                )
            except ValueError:
                date = date.replace(
                    year=date.year + 1,
                    day=28
                )

        return date.strftime("%Y-%m-%d")

    @staticmethod
    def _days_in_month(year, month):
        if month == 12:
            next_month = datetime(
                year + 1,
                1,
                1
            )
        else:
            next_month = datetime(
                year,
                month + 1,
                1
            )

        current_month = datetime(
            year,
            month,
            1
        )

        return (next_month - current_month).days

    @staticmethod
    def _validate_description(description):
        if not isinstance(description, str):
            raise ValueError(
                "Description must be text."
            )

        if not description.strip():
            raise ValueError(
                "Description cannot be empty."
            )

    @staticmethod
    def _validate_amount(amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(
                "Amount must be a number."
            )

        if amount < 0:
            raise ValueError(
                "Amount cannot be negative."
            )

    @staticmethod
    def _validate_category(category):
        if not isinstance(category, str):
            raise ValueError(
                "Category must be text."
            )

        if not category.strip():
            raise ValueError(
                "Category cannot be empty."
            )

    def _validate_frequency(self, frequency):
        if frequency not in self.VALID_FREQUENCIES:
            raise ValueError(
                "Invalid frequency."
            )

    @staticmethod
    def _validate_date(date_value):
        try:
            datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Date must use YYYY-MM-DD format."
            )