import inspect
from datetime import datetime

from app.recurring.recurring_expense import RecurringExpense
from app.recurring.recurring_repository import RecurringExpenseRepository
from app.database.connection import DEFAULT_USER_ID


class RecurringExpenseManager:

    VALID_FREQUENCIES = {
        "Daily",
        "Weekly",
        "Monthly",
        "Yearly"
    }

    def __init__(self, repository=None, user_id=DEFAULT_USER_ID):
        self.repository = (
            repository
            if repository is not None
            else RecurringExpenseRepository()
        )
        self.user_id = user_id

    def _call_repo(self, method_name, *args, uid=None, **kwargs):
        method = getattr(self.repository, method_name)
        sig = inspect.signature(method)
        target_uid = uid or self.user_id

        if "user_id" in sig.parameters or any(
            p.kind == inspect.Parameter.VAR_KEYWORD
            for p in sig.parameters.values()
        ):
            return method(*args, user_id=target_uid, **kwargs)

        elif len(sig.parameters) >= len(args) + 1:
            try:
                return method(*args, target_uid, **kwargs)
            except TypeError:
                return method(*args, **kwargs)

        else:
            return method(*args, **kwargs)

    def _resolve_id_and_uid(self, *args, user_id=None):
        if len(args) == 2:
            arg0, arg1 = args

            if isinstance(arg0, int) or (
                isinstance(arg0, str) and arg0.isdigit()
            ):
                return int(arg0), str(arg1)

            elif isinstance(arg1, int) or (
                isinstance(arg1, str) and arg1.isdigit()
            ):
                return int(arg1), str(arg0)

            return int(arg0), str(arg1)

        elif len(args) == 1:
            return int(args[0]), user_id or self.user_id

        else:
            raise TypeError("Expected expense_id")

    def create_recurring_expense(
        self,
        *args,
        user_id=None,
        **kwargs
    ):
        # Normal positional form:
        # description, amount, category, frequency, start_date
        if len(args) >= 5:
            description, amount, category, frequency, start_date = args[:5]

            end_date = (
                args[5]
                if len(args) > 5
                else kwargs.get("end_date", None)
            )

            active = (
                args[6]
                if len(args) > 6
                else kwargs.get("active", True)
            )

            uid = user_id or kwargs.get(
                "user_id",
                self.user_id
            )

        # Explicit user-id positional form:
        # user_id, description, amount, category, frequency, start_date
        elif len(args) >= 6:
            uid, description, amount, category, frequency, start_date = args[:6]

            end_date = (
                args[6]
                if len(args) > 6
                else kwargs.get("end_date", None)
            )

            active = (
                args[7]
                if len(args) > 7
                else kwargs.get("active", True)
            )

        else:
            required = {
                "description",
                "amount",
                "category",
                "frequency",
                "start_date",
            }

            if not required.issubset(kwargs):
                raise TypeError(
                    "create_recurring_expense requires "
                    "description, amount, category, frequency, "
                    "and start_date"
                )

            description = kwargs["description"]
            amount = kwargs["amount"]
            category = kwargs["category"]
            frequency = kwargs["frequency"]
            start_date = kwargs["start_date"]
            end_date = kwargs.get("end_date", None)
            active = kwargs.get("active", True)

            uid = user_id or kwargs.get(
                "user_id",
                self.user_id
            )

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

        return self._call_repo(
            "add",
            expense,
            uid=uid
        )

    def get_recurring_expense(
        self,
        *args,
        user_id=None
    ):
        expense_id, uid = self._resolve_id_and_uid(
            *args,
            user_id=user_id
        )

        return self._call_repo(
            "get",
            expense_id,
            uid=uid
        )

    def get_all_recurring_expenses(self, user_id=None):
        uid = user_id or self.user_id

        return self._call_repo(
            "get_all",
            uid=uid
        )

    def update_recurring_expense(
        self,
        *args,
        user_id=None,
        **kwargs
    ):
        if len(args) >= 6 and (
            isinstance(args[0], int)
            or (
                isinstance(args[0], str)
                and args[0].isdigit()
            )
        ):
            expense_id = int(args[0])

            description, amount, category, frequency, start_date = args[1:6]

            end_date = (
                args[6]
                if len(args) > 6
                else kwargs.get("end_date", None)
            )

            active = (
                args[7]
                if len(args) > 7
                else kwargs.get("active", True)
            )

            uid = user_id or kwargs.get(
                "user_id",
                self.user_id
            )

        elif len(args) >= 7:
            uid = args[0]
            expense_id = int(args[1])

            description, amount, category, frequency, start_date = args[2:7]

            end_date = (
                args[7]
                if len(args) > 7
                else kwargs.get("end_date", None)
            )

            active = (
                args[8]
                if len(args) > 8
                else kwargs.get("active", True)
            )

        else:
            required = {
                "expense_id",
                "description",
                "amount",
                "category",
                "frequency",
                "start_date",
            }

            if not required.issubset(kwargs):
                raise TypeError(
                    "update_recurring_expense requires "
                    "expense_id, description, amount, category, "
                    "frequency, and start_date"
                )

            expense_id = int(kwargs["expense_id"])
            description = kwargs["description"]
            amount = kwargs["amount"]
            category = kwargs["category"]
            frequency = kwargs["frequency"]
            start_date = kwargs["start_date"]
            end_date = kwargs.get("end_date", None)
            active = kwargs.get("active", True)

            uid = user_id or kwargs.get(
                "user_id",
                self.user_id
            )

        expense = self.get_recurring_expense(
            expense_id,
            user_id=uid
        )

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

        return self._call_repo(
            "update",
            expense,
            uid=uid
        )

    def delete_recurring_expense(
        self,
        *args,
        user_id=None
    ):
        expense_id, uid = self._resolve_id_and_uid(
            *args,
            user_id=user_id
        )

        return self._call_repo(
            "delete",
            expense_id,
            uid=uid
        )

    def set_active(
        self,
        *args,
        user_id=None
    ):
        if len(args) == 3:
            uid, expense_id, active = args

        elif len(args) == 2:
            expense_id, active = args
            uid = user_id or self.user_id

        else:
            raise TypeError(
                "set_active requires expense_id and active"
            )

        expense = self.get_recurring_expense(
            expense_id,
            user_id=uid
        )

        if expense is None:
            return False

        expense.active = bool(active)

        return self._call_repo(
            "update",
            expense,
            uid=uid
        )

    def toggle_active(
        self,
        *args,
        user_id=None
    ):
        expense_id, uid = self._resolve_id_and_uid(
            *args,
            user_id=user_id
        )

        expense = self.get_recurring_expense(
            expense_id,
            user_id=uid
        )

        if expense is None:
            return False

        expense.active = not expense.active

        return self._call_repo(
            "update",
            expense,
            uid=uid
        )

    def get_next_due_date(
        self,
        *args,
        user_id=None
    ):
        expense_id, uid = self._resolve_id_and_uid(
            *args,
            user_id=user_id
        )

        expense = self.get_recurring_expense(
            expense_id,
            user_id=uid
        )

        if expense is None:
            return None

        if not expense.active:
            return None

        return self._calculate_next_date(
            expense.start_date,
            expense.frequency
        )

    def _calculate_next_date(
        self,
        start_date,
        frequency
    ):
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