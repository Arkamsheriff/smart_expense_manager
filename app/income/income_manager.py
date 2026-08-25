from app.income.income import Income
from app.income.income_repository import IncomeRepository


class IncomeManager:

    def __init__(self, repository=None):
        self.repository = repository or IncomeRepository()
        self.repository.initialize_table()

    def create_income(
        self,
        description,
        amount,
        category
    ):
        income = Income(
            None,
            description,
            amount,
            category
        )

        return self.repository.add(income)

    def get_income(self, income_id):
        return self.repository.get_by_id(income_id)

    def get_all_income(self):
        return self.repository.get_all()

    def update_income(
        self,
        income_id,
        description,
        amount,
        category
    ):
        income = self.repository.get_by_id(income_id)

        if income is None:
            return False

        income.description = description
        income.amount = float(amount)
        income.category = category

        return self.repository.update(income)

    def delete_income(self, income_id):
        return self.repository.delete(income_id)

    def total_income(self):
        return self.repository.total()

    def get_income_by_category(self, category):
        return self.repository.get_by_category(category)