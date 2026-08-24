from datetime import datetime

from app.goals.goal import Goal


def test_goal_creation():
    goal = Goal(
        1,
        "Emergency Fund",
        100000.00
    )

    assert goal.id == 1
    assert goal.name == "Emergency Fund"
    assert goal.target_amount == 100000.00
    assert goal.current_amount == 0.0
    assert isinstance(goal.created_at, datetime)


def test_goal_creation_with_current_amount():
    goal = Goal(
        1,
        "New Car",
        1000000.00,
        250000.00
    )

    assert goal.target_amount == 1000000.00
    assert goal.current_amount == 250000.00


def test_goal_creation_with_target_date():
    goal = Goal(
        1,
        "Vacation",
        50000.00,
        10000.00,
        "2027-01-01"
    )

    assert goal.target_date == "2027-01-01"