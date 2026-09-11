import inspect
from app.income.income import Income
from app.income.income_repository import IncomeRepository
from app.database.connection import DEFAULT_USER_ID


class IncomeManager:

    def __init__(self, repository=None, user_id=DEFAULT_USER_ID):
        self.repository = repository or IncomeRepository()
        self.user_id = user_id
        if hasattr(self.repository, "initialize_table"):
            self.repository.initialize_table()

    def _call_repo(self, method_name, *args, uid=None, **kwargs):
        method = getattr(self.repository, method_name)
        sig = inspect.signature(method)
        target_uid = uid or self.user_id
        if "user_id" in sig.parameters or any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        ):
            return method(*args, user_id=target_uid, **kwargs)
        elif len(sig.parameters) >= len(args) + 1:
            try:
                return method(*args, target_uid, **kwargs)
            except TypeError:
                return method(*args, **kwargs)
        else:
            return method(*args, **kwargs)

    def create_income(self, *args, user_id=None, **kwargs):
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
            raise TypeError("create_income requires description, amount, and category")

        income = Income(
            None,
            description,
            float(amount),
            category
        )

        return self._call_repo("add", income, uid=uid)

    def get_income(self, *args, user_id=None):
        if len(args) == 2:
            uid, income_id = args
        elif len(args) == 1:
            income_id = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("get_income requires income_id")

        return self._call_repo("get_by_id", income_id, uid=uid)

    def get_all_income(self, user_id=None):
        uid = user_id or self.user_id
        return self._call_repo("get_all", uid=uid)

    def update_income(self, *args, user_id=None, **kwargs):
        if len(args) == 5:
            uid, income_id, description, amount, category = args
        elif len(args) == 4:
            income_id, description, amount, category = args
            uid = user_id or self.user_id
        elif "income_id" in kwargs and "description" in kwargs and "amount" in kwargs and "category" in kwargs:
            income_id = kwargs["income_id"]
            description = kwargs["description"]
            amount = kwargs["amount"]
            category = kwargs["category"]
            uid = user_id or kwargs.get("user_id", self.user_id)
        else:
            raise TypeError("update_income requires income_id, description, amount, and category")

        income = self._call_repo("get_by_id", income_id, uid=uid)

        if income is None:
            return False

        income.description = description
        income.amount = float(amount)
        income.category = category

        return self._call_repo("update", income, uid=uid)

    def delete_income(self, *args, user_id=None):
        if len(args) == 2:
            uid, income_id = args
        elif len(args) == 1:
            income_id = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("delete_income requires income_id")

        return self._call_repo("delete", income_id, uid=uid)

    def total_income(self, user_id=None):
        uid = user_id or self.user_id
        return self._call_repo("total", uid=uid)

    def get_income_by_category(self, *args, user_id=None):
        if len(args) == 2:
            uid, category = args
        elif len(args) == 1:
            category = args[0]
            uid = user_id or self.user_id
        else:
            raise TypeError("get_income_by_category requires category")

        return self._call_repo("get_by_category", category, uid=uid)