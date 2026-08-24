from datetime import datetime

from app.budget.budget import Budget


def test_budget_creation():

    budget = Budget(
        1,
        "2026-08",
        30000.00
    )

    assert budget.id == 1
    assert budget.month == "2026-08"
    assert budget.amount == 30000.00
    assert isinstance(budget.created_at, datetime)


def test_budget_creation_with_created_at():

    created_at = datetime(
        2026,
        8,
        24,
        19,
        30,
        0
    )

    budget = Budget(
        1,
        "2026-08",
        30000.00,
        created_at
    )

    assert budget.created_at == created_at

from app.budget.budget_repository import BudgetRepository


def create_repository(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    repository = BudgetRepository()
    repository.initialize_table()

    return repository


def test_budget_repository_add_and_get_by_month(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    budget = Budget(
        0,
        "2026-08",
        30000.00
    )

    repository.add(budget)

    result = repository.get_by_month("2026-08")

    assert result is not None
    assert result.id == budget.id
    assert result.month == "2026-08"
    assert result.amount == 30000.00


def test_budget_repository_get_missing_month(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    result = repository.get_by_month("2026-08")

    assert result is None


def test_budget_repository_get_all(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    repository.add(
        Budget(
            0,
            "2026-08",
            30000.00
        )
    )

    repository.add(
        Budget(
            0,
            "2026-09",
            35000.00
        )
    )

    budgets = repository.get_all()

    assert len(budgets) == 2
    assert budgets[0].month == "2026-08"
    assert budgets[1].month == "2026-09"


def test_budget_repository_update(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    budget = repository.add(
        Budget(
            0,
            "2026-08",
            30000.00
        )
    )

    budget.amount = 35000.00

    result = repository.update(budget)

    assert result is True

    updated = repository.get_by_month("2026-08")

    assert updated.amount == 35000.00


def test_budget_repository_delete(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    budget = repository.add(
        Budget(
            0,
            "2026-08",
            30000.00
        )
    )

    result = repository.delete(budget.id)

    assert result is True
    assert repository.get_by_month("2026-08") is None


def test_budget_repository_delete_missing(
    tmp_path,
    monkeypatch
):
    repository = create_repository(tmp_path, monkeypatch)

    result = repository.delete(999)

    assert result is False

from app.budget.budget_manager import BudgetManager


def create_manager(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    return BudgetManager()


def test_set_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    budget = manager.set_budget(
        "2026-08",
        30000.00
    )

    assert budget.id == 1
    assert budget.month == "2026-08"
    assert budget.amount == 30000.00


def test_set_budget_updates_existing_budget(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    first = manager.set_budget(
        "2026-08",
        30000.00
    )

    second = manager.set_budget(
        "2026-08",
        35000.00
    )

    assert second.id == first.id
    assert second.amount == 35000.00

    budgets = manager.get_all_budgets()

    assert len(budgets) == 1


def test_get_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.set_budget(
        "2026-08",
        30000.00
    )

    budget = manager.get_budget("2026-08")

    assert budget is not None
    assert budget.amount == 30000.00


def test_get_missing_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    budget = manager.get_budget("2026-08")

    assert budget is None


def test_budget_remaining(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.set_budget(
        "2026-08",
        30000.00
    )

    remaining = manager.budget_remaining(
        "2026-08",
        12000.00
    )

    assert remaining == 18000.00


def test_budget_utilization(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.set_budget(
        "2026-08",
        30000.00
    )

    utilization = manager.budget_utilization(
        "2026-08",
        15000.00
    )

    assert utilization == 50.0


def test_budget_exceeded(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.set_budget(
        "2026-08",
        30000.00
    )

    assert manager.is_budget_exceeded(
        "2026-08",
        35000.00
    ) is True

    assert manager.is_budget_exceeded(
        "2026-08",
        25000.00
    ) is False

def test_update_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    budget = manager.set_budget(
        "2026-08",
        30000.00
    )

    result = manager.update_budget(
        budget.id,
        "2026-08",
        35000.00
    )

    assert result is True

    updated = manager.get_budget("2026-08")

    assert updated.amount == 35000.00

def test_update_nonexistent_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.update_budget(
        999,
        "2026-08",
        30000.00
    )

    assert result is False

def test_delete_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    budget = manager.set_budget(
        "2026-08",
        30000.00
    )

    result = manager.delete_budget(budget.id)

    assert result is True
    assert manager.get_budget("2026-08") is None

def test_delete_nonexistent_budget(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.delete_budget(999)

    assert result is False

def test_budget_remaining_without_budget(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.budget_remaining(
        "2026-08",
        10000.00
    )

    assert result is None

def test_budget_utilization_without_budget(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.budget_utilization(
        "2026-08",
        10000.00
    )

    assert result is None

def test_budget_utilization_zero_budget(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    manager.set_budget(
        "2026-08",
        0
    )

    result = manager.budget_utilization(
        "2026-08",
        1000.00
    )

    assert result == 0

def test_budget_exceeded_without_budget(
    tmp_path,
    monkeypatch
):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.is_budget_exceeded(
        "2026-08",
        10000.00
    )

    assert result is False

