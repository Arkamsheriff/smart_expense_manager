from app.goals.goal import Goal
from app.goals.goal_repository import GoalRepository


class GoalManager:

    def __init__(self):
        self.repository = GoalRepository()

    def create_goal(
        self,
        name,
        target_amount,
        current_amount=0.0,
        target_date=None
    ):
        goal = Goal(
            None,
            name,
            target_amount,
            current_amount,
            target_date
        )

        return self.repository.add(goal)

    def get_goal(self, goal_id):
        return self.repository.get_by_id(goal_id)

    def get_all_goals(self):
        return self.repository.get_all()

    def update_goal(
        self,
        goal_id,
        name,
        target_amount,
        current_amount,
        target_date=None
    ):
        goal = Goal(
            goal_id,
            name,
            target_amount,
            current_amount,
            target_date
        )

        return self.repository.update(goal)

    def delete_goal(self, goal_id):
        return self.repository.delete(goal_id)

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

        progress = (
            goal.current_amount /
            goal.target_amount
        ) * 100

        return min(progress, 100.0)

    def goal_completed(self, goal_id):
        goal = self.get_goal(goal_id)

        if goal is None:
            return False

        return goal.current_amount >= goal.target_amount

    def add_to_goal(self, goal_id, amount):
        goal = self.get_goal(goal_id)

        if goal is None:
            return False

        if amount <= 0:
            return False

        goal.current_amount += amount

        return self.repository.update(goal)