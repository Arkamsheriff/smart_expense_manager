from app.income.income_manager import IncomeManager


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


class FakeIncomeRepository:

    def __init__(self):
        self.incomes = {}
        self.next_id = 1

    def initialize_table(self):
        pass

    def add(self, income, user_id=None):
        income.id = self.next_id

        self.incomes[income.id] = (
            income,
            user_id
        )

        self.next_id += 1

        return income

    def get_by_id(self, income_id, user_id=None):
        record = self.incomes.get(income_id)

        if record is None:
            return None

        income, stored_user_id = record

        if stored_user_id != user_id:
            return None

        return income

    def get_all(self, user_id=None):
        return [
            income
            for income, stored_user_id in self.incomes.values()
            if stored_user_id == user_id
        ]

    def update(self, income, user_id=None):
        record = self.incomes.get(income.id)

        if record is None:
            return False

        _, stored_user_id = record

        if stored_user_id != user_id:
            return False

        self.incomes[income.id] = (
            income,
            user_id
        )

        return True

    def delete(self, income_id, user_id=None):
        record = self.incomes.get(income_id)

        if record is None:
            return False

        _, stored_user_id = record

        if stored_user_id != user_id:
            return False

        del self.incomes[income_id]

        return True

    def total(self, user_id=None):
        return sum(
            income.amount
            for income, stored_user_id in self.incomes.values()
            if stored_user_id == user_id
        )

    def get_by_category(
        self,
        category,
        user_id=None
    ):
        return [
            income
            for income, stored_user_id in self.incomes.values()
            if (
                stored_user_id == user_id
                and income.category.lower() == category.lower()
            )
        ]


def create_manager(user_id=TEST_USER_ID):
    return IncomeManager(
        FakeIncomeRepository(),
        user_id=user_id
    )


def test_create_income():
    manager = create_manager()

    income = manager.create_income(
        TEST_USER_ID,
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
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    income = manager.get_income(
        TEST_USER_ID,
        created.id
    )

    assert income is not None
    assert income.description == "Salary"


def test_get_missing_income():
    manager = create_manager()

    assert manager.get_income(
        TEST_USER_ID,
        999
    ) is None


def test_get_all_income():
    manager = create_manager()

    manager.create_income(
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        TEST_USER_ID,
        "Freelance",
        15000,
        "Freelance"
    )

    incomes = manager.get_all_income(
        TEST_USER_ID
    )

    assert len(incomes) == 2


def test_update_income():
    manager = create_manager()

    income = manager.create_income(
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    result = manager.update_income(
        TEST_USER_ID,
        income.id,
        "Updated Salary",
        55000,
        "Job"
    )

    assert result is True

    updated = manager.get_income(
        TEST_USER_ID,
        income.id
    )

    assert updated.description == "Updated Salary"
    assert updated.amount == 55000.0
    assert updated.category == "Job"


def test_update_missing_income():
    manager = create_manager()

    result = manager.update_income(
        TEST_USER_ID,
        999,
        "Unknown",
        1000,
        "Other"
    )

    assert result is False


def test_delete_income():
    manager = create_manager()

    income = manager.create_income(
        TEST_USER_ID,
        "Bonus",
        10000,
        "Bonus"
    )

    result = manager.delete_income(
        TEST_USER_ID,
        income.id
    )

    assert result is True

    assert manager.get_income(
        TEST_USER_ID,
        income.id
    ) is None


def test_delete_missing_income():
    manager = create_manager()

    assert manager.delete_income(
        TEST_USER_ID,
        999
    ) is False


def test_total_income():
    manager = create_manager()

    manager.create_income(
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        TEST_USER_ID,
        "Freelance",
        15000,
        "Freelance"
    )

    assert manager.total_income(
        TEST_USER_ID
    ) == 65000.0


def test_total_income_empty():
    manager = create_manager()

    assert manager.total_income(
        TEST_USER_ID
    ) == 0


def test_income_by_category():
    manager = create_manager()

    manager.create_income(
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    manager.create_income(
        TEST_USER_ID,
        "Bonus",
        10000,
        "Bonus"
    )

    manager.create_income(
        TEST_USER_ID,
        "Second Salary",
        5000,
        "salary"
    )

    incomes = manager.get_income_by_category(
        TEST_USER_ID,
        "SALARY"
    )

    assert len(incomes) == 2


def test_income_by_category_no_results():
    manager = create_manager()

    manager.create_income(
        TEST_USER_ID,
        "Salary",
        50000,
        "Salary"
    )

    incomes = manager.get_income_by_category(
        TEST_USER_ID,
        "Investment"
    )

    assert incomes == []


def test_income_user_isolation():
    repository = FakeIncomeRepository()

    user_one_manager = IncomeManager(
        repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = IncomeManager(
        repository,
        user_id=OTHER_USER_ID
    )

    user_one_manager.create_income(
        TEST_USER_ID,
        "User One Salary",
        50000,
        "Salary"
    )

    user_two_manager.create_income(
        OTHER_USER_ID,
        "User Two Salary",
        60000,
        "Salary"
    )

    user_one_incomes = user_one_manager.get_all_income(
        TEST_USER_ID
    )

    user_two_incomes = user_two_manager.get_all_income(
        OTHER_USER_ID
    )

    assert len(user_one_incomes) == 1
    assert user_one_incomes[0].description == (
        "User One Salary"
    )

    assert len(user_two_incomes) == 1
    assert user_two_incomes[0].description == (
        "User Two Salary"
    )


def test_user_cannot_update_other_users_income():
    repository = FakeIncomeRepository()

    user_one_manager = IncomeManager(
        repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = IncomeManager(
        repository,
        user_id=OTHER_USER_ID
    )

    income = user_one_manager.create_income(
        TEST_USER_ID,
        "Private Salary",
        50000,
        "Salary"
    )

    result = user_two_manager.update_income(
        OTHER_USER_ID,
        income.id,
        "Hacked Salary",
        999999,
        "Other"
    )

    assert result is False

    original = user_one_manager.get_income(
        TEST_USER_ID,
        income.id
    )

    assert original.description == "Private Salary"
    assert original.amount == 50000.0


def test_user_cannot_delete_other_users_income():
    repository = FakeIncomeRepository()

    user_one_manager = IncomeManager(
        repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = IncomeManager(
        repository,
        user_id=OTHER_USER_ID
    )

    income = user_one_manager.create_income(
        TEST_USER_ID,
        "Private Salary",
        50000,
        "Salary"
    )

    result = user_two_manager.delete_income(
        OTHER_USER_ID,
        income.id
    )

    assert result is False

    original = user_one_manager.get_income(
        TEST_USER_ID,
        income.id
    )

    assert original is not None
    assert original.description == "Private Salary"
