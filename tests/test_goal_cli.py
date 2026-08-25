from app.goals.goal import Goal
from app.goals.goal_cli import (
    display_goal_menu,
    get_goal_id,
    get_goal_name,
    get_amount,
    get_positive_amount,
    get_target_date,
    display_goal,
    display_progress,
    handle_goal_menu,
)


class FakeGoalManager:

    def __init__(self):
        self.goals = {}
        self.next_id = 1

    def create_goal(
        self,
        name,
        target_amount,
        current_amount=0.0,
        target_date=None
    ):
        goal = Goal(
            self.next_id,
            name,
            target_amount,
            current_amount,
            target_date
        )

        self.goals[goal.id] = goal
        self.next_id += 1

        return goal

    def get_goal(self, goal_id):
        return self.goals.get(goal_id)

    def get_all_goals(self):
        return list(self.goals.values())

    def update_goal(
        self,
        goal_id,
        name,
        target_amount,
        current_amount,
        target_date=None
    ):
        goal = self.goals.get(goal_id)

        if goal is None:
            return False

        goal.name = name
        goal.target_amount = target_amount
        goal.current_amount = current_amount
        goal.target_date = target_date

        return True

    def delete_goal(self, goal_id):
        if goal_id not in self.goals:
            return False

        del self.goals[goal_id]
        return True

    def goal_remaining(self, goal_id):
        goal = self.get_goal(goal_id)

        if goal is None:
            return None

        return max(
            goal.target_amount - goal.current_amount,
            0
        )

    def goal_progress(self, goal_id):
        goal = self.get_goal(goal_id)

        if goal is None:
            return None

        if goal.target_amount <= 0:
            return 0.0

        return min(
            goal.current_amount /
            goal.target_amount *
            100,
            100
        )

    def goal_completed(self, goal_id):
        goal = self.get_goal(goal_id)

        if goal is None:
            return False

        return (
            goal.current_amount >=
            goal.target_amount
        )

    def add_to_goal(self, goal_id, amount):
        goal = self.get_goal(goal_id)

        if goal is None or amount <= 0:
            return False

        goal.current_amount += amount

        return True


def test_display_goal_menu(capsys):
    display_goal_menu()

    output = capsys.readouterr().out

    assert "GOAL MANAGEMENT" in output
    assert "Create Goal" in output
    assert "View Goal" in output
    assert "Add Money to Goal" in output
    assert "Back" in output


def test_get_goal_id_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "5"
    )

    assert get_goal_id() == 5


def test_get_goal_id_invalid_then_valid(monkeypatch):
    inputs = iter([
        "abc",
        "-1",
        "3"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_goal_id() == 3


def test_get_goal_name_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Emergency Fund"
    )

    assert get_goal_name() == "Emergency Fund"


def test_get_goal_name_empty_then_valid(monkeypatch):
    inputs = iter([
        "",
        "Vacation"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_goal_name() == "Vacation"


def test_get_amount_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "50000"
    )

    assert get_amount("Amount: ") == 50000.0


def test_get_amount_invalid_then_valid(monkeypatch):
    inputs = iter([
        "abc",
        "-100",
        "25000"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_amount("Amount: ") == 25000.0


def test_get_positive_amount(monkeypatch):
    inputs = iter([
        "0",
        "-10",
        "5000"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_positive_amount("Amount: ") == 5000.0


def test_get_target_date_valid(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2027-06"
    )

    assert get_target_date() == "2027-06"


def test_get_target_date_blank(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: ""
    )

    assert get_target_date() is None


def test_get_target_date_invalid_then_valid(monkeypatch):
    inputs = iter([
        "2027-15",
        "invalid",
        "2027-12"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    assert get_target_date() == "2027-12"


def test_display_goal(capsys):
    goal = Goal(
        1,
        "Emergency Fund",
        100000,
        25000,
        "2027-06"
    )

    display_goal(goal)

    output = capsys.readouterr().out

    assert "Emergency Fund" in output
    assert "100000.00" in output
    assert "25000.00" in output
    assert "2027-06" in output


def test_display_progress(capsys):
    goal = Goal(
        1,
        "Emergency Fund",
        100000,
        25000
    )

    display_progress(
        goal,
        25.0,
        75000.0
    )

    output = capsys.readouterr().out

    assert "Emergency Fund" in output
    assert "25.00%" in output
    assert "75000.00" in output
    assert "IN PROGRESS" in output


def test_display_progress_completed(capsys):
    goal = Goal(
        1,
        "Emergency Fund",
        100000,
        100000
    )

    display_progress(
        goal,
        100.0,
        0.0
    )

    output = capsys.readouterr().out

    assert "GOAL COMPLETED" in output


def test_handle_goal_back(monkeypatch):
    manager = FakeGoalManager()

    inputs = iter(["9"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)


def test_handle_goal_invalid_choice(monkeypatch, capsys):
    manager = FakeGoalManager()

    inputs = iter([
        "99",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "Invalid choice." in output


def test_handle_goal_create(monkeypatch):
    manager = FakeGoalManager()

    inputs = iter([
        "1",
        "Emergency Fund",
        "100000",
        "10000",
        "2027-06",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    goal = manager.get_goal(1)

    assert goal.name == "Emergency Fund"
    assert goal.target_amount == 100000
    assert goal.current_amount == 10000
    assert goal.target_date == "2027-06"


def test_handle_goal_view(monkeypatch, capsys):
    manager = FakeGoalManager()

    manager.create_goal(
        "Vacation",
        50000,
        10000,
        "2027-12"
    )

    inputs = iter([
        "2",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "Vacation" in output
    assert "50000.00" in output


def test_handle_goal_view_all(monkeypatch, capsys):
    manager = FakeGoalManager()

    manager.create_goal(
        "Emergency Fund",
        100000,
        25000
    )

    manager.create_goal(
        "Vacation",
        50000,
        10000
    )

    inputs = iter([
        "3",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "Emergency Fund" in output
    assert "Vacation" in output


def test_handle_goal_view_all_empty(monkeypatch, capsys):
    manager = FakeGoalManager()

    inputs = iter([
        "3",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "No goals found." in output


def test_handle_goal_update(monkeypatch):
    manager = FakeGoalManager()

    manager.create_goal(
        "Laptop",
        80000,
        10000
    )

    inputs = iter([
        "4",
        "1",
        "New Laptop",
        "100000",
        "25000",
        "2027-06",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    goal = manager.get_goal(1)

    assert goal.name == "New Laptop"
    assert goal.target_amount == 100000
    assert goal.current_amount == 25000


def test_handle_goal_add_money(monkeypatch):
    manager = FakeGoalManager()

    manager.create_goal(
        "Emergency Fund",
        100000,
        10000
    )

    inputs = iter([
        "5",
        "1",
        "15000",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    goal = manager.get_goal(1)

    assert goal.current_amount == 25000


def test_handle_goal_progress(monkeypatch, capsys):
    manager = FakeGoalManager()

    manager.create_goal(
        "Emergency Fund",
        100000,
        25000
    )

    inputs = iter([
        "6",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "25.00%" in output
    assert "75000.00" in output


def test_handle_goal_status(monkeypatch, capsys):
    manager = FakeGoalManager()

    manager.create_goal(
        "Vacation",
        50000,
        25000
    )

    inputs = iter([
        "7",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "still in progress" in output
    assert "25000.00" in output


def test_handle_goal_completed_status(monkeypatch, capsys):
    manager = FakeGoalManager()

    manager.create_goal(
        "Laptop",
        80000,
        80000
    )

    inputs = iter([
        "7",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "has been completed" in output


def test_handle_goal_delete(monkeypatch):
    manager = FakeGoalManager()

    manager.create_goal(
        "Vacation",
        50000
    )

    inputs = iter([
        "8",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    assert manager.get_goal(1) is None


def test_handle_goal_missing_goal(monkeypatch, capsys):
    manager = FakeGoalManager()

    inputs = iter([
        "2",
        "999",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    handle_goal_menu(manager)

    output = capsys.readouterr().out

    assert "Goal not found." in output