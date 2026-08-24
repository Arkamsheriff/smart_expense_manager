from app.goals.goal import Goal
from app.goals.goal_repository import GoalRepository


def test_goal_repository_add_and_get(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    goal = Goal(
        None,
        "Emergency Fund",
        100000.00
    )

    created = repository.add(goal)

    assert created.id is not None

    retrieved = repository.get_by_id(created.id)

    assert retrieved is not None
    assert retrieved.name == "Emergency Fund"
    assert retrieved.target_amount == 100000.00
    assert retrieved.current_amount == 0.0


def test_goal_repository_get_missing(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    assert repository.get_by_id(999) is None


def test_goal_repository_get_all(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    repository.add(
        Goal(None, "Emergency Fund", 100000)
    )

    repository.add(
        Goal(None, "Vacation", 50000)
    )

    goals = repository.get_all()

    assert len(goals) == 2
    assert goals[0].name == "Emergency Fund"
    assert goals[1].name == "Vacation"


def test_goal_repository_update(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    goal = repository.add(
        Goal(None, "Emergency Fund", 100000)
    )

    goal.name = "Emergency Savings"
    goal.target_amount = 150000
    goal.current_amount = 25000

    assert repository.update(goal) is True

    updated = repository.get_by_id(goal.id)

    assert updated.name == "Emergency Savings"
    assert updated.target_amount == 150000
    assert updated.current_amount == 25000


def test_goal_repository_update_missing(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    goal = Goal(
        999,
        "Missing Goal",
        10000
    )

    assert repository.update(goal) is False


def test_goal_repository_delete(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    goal = repository.add(
        Goal(None, "Vacation", 50000)
    )

    assert repository.delete(goal.id) is True
    assert repository.get_by_id(goal.id) is None


def test_goal_repository_delete_missing(monkeypatch, tmp_path):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(test_database)
    )

    repository = GoalRepository()

    assert repository.delete(999) is False