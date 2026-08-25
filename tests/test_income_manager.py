from app.income.income_manager import IncomeManager


class FakeIncomeRepository:

    def __init__(self):
        self.incomes = {}
        self.next_id = 1

    def initialize_table(self):
        pass

    def add(self, income):
        income.id = self.next_id
        self.incomes[income.id] = income
        self.next_id += 1
        return income

    def get_by_id(self, income_id):
        return self.incomes.get(income_id)

    def get_all(self):
        return list(self.incomes.values())

    def update(self, income):
        if income.id not in self.incomes:
            return False

        self.incomes[income.id] = income
        return True

    def delete(self, income_id):
        if income_id not in self.incomes:
            return False

        del self.incomes[income_id]
        return True

    def total(self):
        return sum(
            income.amount
            for income in self.incomes.values()
        )

    def get_by_category(self, category):
        return [
            income
            for income in self.incomes.values()
            if income.category.lower() == category.lower()
        ]


def create_manager():
    return IncomeManager(
        FakeIncomeRepository()
    )


def test_create_income():
    manager = create_manager()

    income = manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    assert income.id == 1
    assert income.description == "Salary"
    assert income.amount == 50000.0
    assert income.category == "Salary"


def test_get_income():
    manager = create_manager()

    created = manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    income = manager.get_income(created.id)

    assert income is not None
    assert income.description == "Salary"


def test_get_missing_income():
    manager = create_manager()

    assert manager.get_income(999) is None


def test_get_all_income():
    manager = create_manager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Freelance",
        15000,
        "Freelance"
    )

    incomes = manager.get_all_income()

    assert len(incomes) == 2


def test_update_income():
    manager = create_manager()

    income = manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    result = manager.update_income(
        income.id,
        "Updated Salary",
        55000,
        "Job"
    )

    assert result is True

    updated = manager.get_income(income.id)

    assert updated.description == "Updated Salary"
    assert updated.amount == 55000.0
    assert updated.category == "Job"


def test_update_missing_income():
    manager = create_manager()

    result = manager.update_income(
        999,
        "Unknown",
        1000,
        "Other"
    )

    assert result is False


def test_delete_income():
    manager = create_manager()

    income = manager.create_income(
        "Bonus",
        10000,
        "Bonus"
    )

    result = manager.delete_income(income.id)

    assert result is True
    assert manager.get_income(income.id) is None


def test_delete_missing_income():
    manager = create_manager()

    assert manager.delete_income(999) is False


def test_total_income():
    manager = create_manager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Freelance",
        15000,
        "Freelance"
    )

    assert manager.total_income() == 65000.0


def test_total_income_empty():
    manager = create_manager()

    assert manager.total_income() == 0


def test_income_by_category():
    manager = create_manager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        "Bonus",
        10000,
        "Bonus"
    )

    manager.create_income(
        "Second Salary",
        5000,
        "salary"
    )

    incomes = manager.get_income_by_category(
        "SALARY"
    )

    assert len(incomes) == 2


def test_income_by_category_no_results():
    manager = create_manager()

    manager.create_income(
        "Salary",
        50000,
        "Salary"
    )

    incomes = manager.get_income_by_category(
        "Investment"
    )

    assert incomes == []