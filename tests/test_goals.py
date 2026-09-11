from app.goals.goal import Goal
from app.goals.goal_repository import GoalRepository
from app.goals.goal_manager import GoalManager


TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
OTHER_USER_ID = "00000000-0000-0000-0000-000000000002"


def create_repository(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setenv(
        "USE_POSTGRES",
        "false"
    )

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    return GoalRepository()


def create_manager(
    tmp_path,
    monkeypatch,
    user_id=TEST_USER_ID
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    return GoalManager(
        repository=repository,
        user_id=user_id
    )


def test_goal_creation():
    goal = Goal(
        None,
        "New Car",
        100000.00,
        10000.00,
        "2027-01-01"
    )

    assert goal.id is None
    assert goal.name == "New Car"
    assert goal.target_amount == 100000.00
    assert goal.current_amount == 10000.00
    assert goal.target_date == "2027-01-01"


def test_create_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00,
        "2027-01-01"
    )

    assert goal.id == 1
    assert goal.name == "New Car"
    assert goal.target_amount == 100000.00
    assert goal.current_amount == 10000.00
    assert goal.target_date == "2027-01-01"


def test_get_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    created = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00,
        "2027-01-01"
    )

    goal = manager.get_goal(
        TEST_USER_ID,
        created.id
    )

    assert goal is not None
    assert goal.name == "New Car"


def test_get_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.get_goal(
        TEST_USER_ID,
        99999
    )

    assert goal is None


def test_get_all_goals(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    manager.create_goal(
        TEST_USER_ID,
        "Vacation",
        50000.00,
        5000.00
    )

    goals = manager.get_all_goals(
        TEST_USER_ID
    )

    assert len(goals) == 2
    assert goals[0].name == "New Car"
    assert goals[1].name == "Vacation"


def test_update_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    result = manager.update_goal(
        TEST_USER_ID,
        goal.id,
        "Updated Car",
        150000.00,
        20000.00,
        "2027-06-01"
    )

    assert result is True

    updated = manager.get_goal(
        TEST_USER_ID,
        goal.id
    )

    assert updated.name == "Updated Car"
    assert updated.target_amount == 150000.00
    assert updated.current_amount == 20000.00
    assert updated.target_date == "2027-06-01"


def test_update_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    result = manager.update_goal(
        TEST_USER_ID,
        99999,
        "Unknown",
        50000.00,
        0.00
    )

    assert result is False


def test_delete_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    result = manager.delete_goal(
        TEST_USER_ID,
        goal.id
    )

    assert result is True

    assert manager.get_goal(
        TEST_USER_ID,
        goal.id
    ) is None


def test_delete_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    result = manager.delete_goal(
        TEST_USER_ID,
        99999
    )

    assert result is False


def test_goal_remaining(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        25000.00
    )

    remaining = manager.goal_remaining(
        TEST_USER_ID,
        goal.id
    )

    assert remaining == 75000.00


def test_goal_remaining_completed(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        120000.00
    )

    remaining = manager.goal_remaining(
        TEST_USER_ID,
        goal.id
    )

    assert remaining == 0.0


def test_goal_remaining_missing(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    result = manager.goal_remaining(
        TEST_USER_ID,
        99999
    )

    assert result is None


def test_goal_progress(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        25000.00
    )

    progress = manager.goal_progress(
        TEST_USER_ID,
        goal.id
    )

    assert progress == 25.0


def test_goal_progress_capped_at_100(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        120000.00
    )

    progress = manager.goal_progress(
        TEST_USER_ID,
        goal.id
    )

    assert progress == 100.0


def test_goal_progress_zero_target(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "Zero Goal",
        0.00,
        0.00
    )

    progress = manager.goal_progress(
        TEST_USER_ID,
        goal.id
    )

    assert progress == 0.0


def test_goal_progress_missing(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    result = manager.goal_progress(
        TEST_USER_ID,
        99999
    )

    assert result is None


def test_goal_completed(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        100000.00
    )

    assert manager.goal_completed(
        TEST_USER_ID,
        goal.id
    ) is True


def test_goal_not_completed(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        50000.00
    )

    assert manager.goal_completed(
        TEST_USER_ID,
        goal.id
    ) is False


def test_goal_completed_missing(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    assert manager.goal_completed(
        TEST_USER_ID,
        99999
    ) is False


def test_add_to_goal(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        TEST_USER_ID,
        goal.id,
        15000.00
    )

    assert result is True

    updated = manager.get_goal(
        TEST_USER_ID,
        goal.id
    )

    assert updated.current_amount == 25000.00


def test_add_to_goal_missing(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    result = manager.add_to_goal(
        TEST_USER_ID,
        99999,
        10000.00
    )

    assert result is False


def test_add_to_goal_rejects_zero(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        TEST_USER_ID,
        goal.id,
        0
    )

    assert result is False


def test_add_to_goal_rejects_negative(tmp_path, monkeypatch):
    manager = create_manager(
        tmp_path,
        monkeypatch
    )

    goal = manager.create_goal(
        TEST_USER_ID,
        "New Car",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        TEST_USER_ID,
        goal.id,
        -5000
    )

    assert result is False


def test_goal_repository_user_isolation(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    repository.add(
        Goal(
            None,
            "Private Goal",
            100000.00,
            10000.00
        ),
        TEST_USER_ID
    )

    user_one_goals = repository.get_all(
        TEST_USER_ID
    )

    user_two_goals = repository.get_all(
        OTHER_USER_ID
    )

    assert len(user_one_goals) == 1
    assert len(user_two_goals) == 0


def test_user_cannot_update_other_users_goal(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    goal = repository.add(
        Goal(
            None,
            "Private Goal",
            100000.00,
            10000.00
        ),
        TEST_USER_ID
    )

    goal.name = "Hacked Goal"
    goal.target_amount = 999999.00

    result = repository.update(
        goal,
        OTHER_USER_ID
    )

    assert result is False

    original = repository.get_by_id(
        goal.id,
        TEST_USER_ID
    )

    assert original.name == "Private Goal"
    assert original.target_amount == 100000.00


def test_user_cannot_delete_other_users_goal(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    goal = repository.add(
        Goal(
            None,
            "Private Goal",
            100000.00,
            10000.00
        ),
        TEST_USER_ID
    )

    result = repository.delete(
        goal.id,
        OTHER_USER_ID
    )

    assert result is False

    original = repository.get_by_id(
        goal.id,
        TEST_USER_ID
    )

    assert original is not None


def test_manager_user_isolation(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    user_one_manager = GoalManager(
        repository=repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = GoalManager(
        repository=repository,
        user_id=OTHER_USER_ID
    )

    user_one_manager.create_goal(
        TEST_USER_ID,
        "User One Goal",
        100000.00,
        10000.00
    )

    user_two_goals = user_two_manager.get_all_goals(
        OTHER_USER_ID
    )

    assert user_two_goals == []


def test_user_cannot_update_other_users_goal_through_manager(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    user_one_manager = GoalManager(
        repository=repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = GoalManager(
        repository=repository,
        user_id=OTHER_USER_ID
    )

    goal = user_one_manager.create_goal(
        TEST_USER_ID,
        "Private Goal",
        100000.00,
        10000.00
    )

    result = user_two_manager.update_goal(
        OTHER_USER_ID,
        goal.id,
        "Hacked Goal",
        999999.00,
        999999.00
    )

    assert result is False

    original = user_one_manager.get_goal(
        TEST_USER_ID,
        goal.id
    )

    assert original.name == "Private Goal"
    assert original.target_amount == 100000.00


def test_user_cannot_delete_other_users_goal_through_manager(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    user_one_manager = GoalManager(
        repository=repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = GoalManager(
        repository=repository,
        user_id=OTHER_USER_ID
    )

    goal = user_one_manager.create_goal(
        TEST_USER_ID,
        "Private Goal",
        100000.00,
        10000.00
    )

    result = user_two_manager.delete_goal(
        OTHER_USER_ID,
        goal.id
    )

    assert result is False

    original = user_one_manager.get_goal(
        TEST_USER_ID,
        goal.id
    )

    assert original is not None


def test_user_cannot_add_to_other_users_goal(
    tmp_path,
    monkeypatch
):
    repository = create_repository(
        tmp_path,
        monkeypatch
    )

    user_one_manager = GoalManager(
        repository=repository,
        user_id=TEST_USER_ID
    )

    user_two_manager = GoalManager(
        repository=repository,
        user_id=OTHER_USER_ID
    )

    goal = user_one_manager.create_goal(
        TEST_USER_ID,
        "Private Goal",
        100000.00,
        10000.00
    )

    result = user_two_manager.add_to_goal(
        OTHER_USER_ID,
        goal.id,
        50000.00
    )

    assert result is False

    original = user_one_manager.get_goal(
        TEST_USER_ID,
        goal.id
    )

    assert original.current_amount == 10000.00
