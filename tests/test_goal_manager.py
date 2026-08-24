from app.goals.goal_manager import GoalManager


def create_manager(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        str(database_path)
    )

    return GoalManager()


def test_create_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00
    )

    assert goal.id == 1
    assert goal.name == "Emergency Fund"
    assert goal.target_amount == 100000.00
    assert goal.current_amount == 0.0


def test_create_goal_with_current_amount(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Vacation",
        50000.00,
        10000.00
    )

    assert goal.current_amount == 10000.00


def test_get_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    created = manager.create_goal(
        "Laptop",
        80000.00
    )

    goal = manager.get_goal(created.id)

    assert goal is not None
    assert goal.name == "Laptop"
    assert goal.target_amount == 80000.00


def test_get_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.get_goal(999)

    assert result is None


def test_get_all_goals(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    manager.create_goal(
        "Emergency Fund",
        100000.00
    )

    manager.create_goal(
        "Vacation",
        50000.00
    )

    goals = manager.get_all_goals()

    assert len(goals) == 2
    assert goals[0].name == "Emergency Fund"
    assert goals[1].name == "Vacation"


def test_update_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Laptop",
        80000.00
    )

    result = manager.update_goal(
        goal.id,
        "New Laptop",
        100000.00,
        25000.00,
        "2027-06-01"
    )

    assert result is True

    updated = manager.get_goal(goal.id)

    assert updated.name == "New Laptop"
    assert updated.target_amount == 100000.00
    assert updated.current_amount == 25000.00
    assert updated.target_date == "2027-06-01"


def test_update_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.update_goal(
        999,
        "Missing Goal",
        10000.00,
        0.00
    )

    assert result is False


def test_delete_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Vacation",
        50000.00
    )

    result = manager.delete_goal(goal.id)

    assert result is True
    assert manager.get_goal(goal.id) is None


def test_delete_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.delete_goal(999)

    assert result is False


def test_goal_remaining(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        25000.00
    )

    remaining = manager.goal_remaining(goal.id)

    assert remaining == 75000.00


def test_goal_remaining_when_completed(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Vacation",
        50000.00,
        60000.00
    )

    remaining = manager.goal_remaining(goal.id)

    assert remaining == 0


def test_goal_remaining_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.goal_remaining(999)

    assert result is None


def test_goal_progress(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        25000.00
    )

    progress = manager.goal_progress(goal.id)

    assert progress == 25.0


def test_goal_progress_completed(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Vacation",
        50000.00,
        50000.00
    )

    progress = manager.goal_progress(goal.id)

    assert progress == 100.0


def test_goal_progress_capped_at_100(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Vacation",
        50000.00,
        60000.00
    )

    progress = manager.goal_progress(goal.id)

    assert progress == 100.0


def test_goal_progress_zero_target(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Zero Goal",
        0.00,
        0.00
    )

    progress = manager.goal_progress(goal.id)

    assert progress == 0.0


def test_goal_progress_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.goal_progress(999)

    assert result is None


def test_goal_completed(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        100000.00
    )

    assert manager.goal_completed(goal.id) is True


def test_goal_not_completed(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        25000.00
    )

    assert manager.goal_completed(goal.id) is False


def test_goal_completed_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    assert manager.goal_completed(999) is False


def test_add_to_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        goal.id,
        15000.00
    )

    assert result is True

    updated = manager.get_goal(goal.id)

    assert updated.current_amount == 25000.00


def test_add_to_missing_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    result = manager.add_to_goal(
        999,
        10000.00
    )

    assert result is False


def test_add_negative_amount_to_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        goal.id,
        -5000.00
    )

    assert result is False

    updated = manager.get_goal(goal.id)

    assert updated.current_amount == 10000.00


def test_add_zero_amount_to_goal(tmp_path, monkeypatch):
    manager = create_manager(tmp_path, monkeypatch)

    goal = manager.create_goal(
        "Emergency Fund",
        100000.00,
        10000.00
    )

    result = manager.add_to_goal(
        goal.id,
        0.00
    )

    assert result is False

    updated = manager.get_goal(goal.id)

    assert updated.current_amount == 10000.00