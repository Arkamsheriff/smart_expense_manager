from app.goals.goal import Goal
from app.goals.goal_repository import GoalRepository
from app.database.connection import DEFAULT_USER_ID


class GoalManager:

    def __init__(self, repository=None, user_id=DEFAULT_USER_ID):
        self.repository = repository or GoalRepository()
        self.user_id = user_id

    def _resolve_id_and_uid(self, *args, user_id=None):
        if len(args) == 2:
            arg0, arg1 = args
            if isinstance(arg0, int) or (isinstance(arg0, str) and arg0.isdigit()):
                return int(arg0), str(arg1)
            elif isinstance(arg1, int) or (isinstance(arg1, str) and arg1.isdigit()):
                return int(arg1), str(arg0)
            return int(arg0), str(arg1)
        elif len(args) == 1:
            return int(args[0]), user_id or self.user_id
        else:
            raise TypeError("Expected goal_id")

    def create_goal(
        self,
        *args,
        user_id=None,
        **kwargs
    ):
        if len(args) >= 2 and isinstance(args[1], (int, float)):
            name = args[0]
            target_amount = args[1]
            current_amount = args[2] if len(args) > 2 else kwargs.get("current_amount", 0.0)
            target_date = args[3] if len(args) > 3 else kwargs.get("target_date", None)
            uid = user_id or kwargs.get("user_id", self.user_id)
        elif len(args) >= 3 and isinstance(args[2], (int, float)):
            uid = args[0]
            name = args[1]
            target_amount = args[2]
            current_amount = args[3] if len(args) > 3 else kwargs.get("current_amount", 0.0)
            target_date = args[4] if len(args) > 4 else kwargs.get("target_date", None)
        else:
            name = kwargs["name"]
            target_amount = kwargs["target_amount"]
            current_amount = kwargs.get("current_amount", 0.0)
            target_date = kwargs.get("target_date", None)
            uid = user_id or kwargs.get("user_id", self.user_id)

        goal = Goal(
            None,
            name,
            float(target_amount),
            float(current_amount),
            target_date
        )

        return self.repository.add(
            goal,
            uid
        )

    def get_goal(self, *args, user_id=None):
        goal_id, uid = self._resolve_id_and_uid(*args, user_id=user_id)
        return self.repository.get_by_id(
            goal_id,
            uid
        )

    def get_all_goals(self, user_id=None):
        uid = user_id or self.user_id
        return self.repository.get_all(uid)

    def update_goal(
        self,
        *args,
        user_id=None,
        **kwargs
    ):
        if len(args) >= 4 and isinstance(args[0], int):
            goal_id, name, target_amount, current_amount = args[:4]
            target_date = args[4] if len(args) > 4 else kwargs.get("target_date", None)
            uid = user_id or kwargs.get("user_id", self.user_id)
        elif len(args) >= 5 and isinstance(args[1], int):
            uid, goal_id, name, target_amount, current_amount = args[:5]
            target_date = args[5] if len(args) > 5 else kwargs.get("target_date", None)
        else:
            goal_id = kwargs["goal_id"]
            name = kwargs["name"]
            target_amount = kwargs["target_amount"]
            current_amount = kwargs["current_amount"]
            target_date = kwargs.get("target_date", None)
            uid = user_id or kwargs.get("user_id", self.user_id)

        goal = Goal(
            goal_id,
            name,
            float(target_amount),
            float(current_amount),
            target_date
        )

        return self.repository.update(
            goal,
            uid
        )

    def delete_goal(self, *args, user_id=None):
        goal_id, uid = self._resolve_id_and_uid(*args, user_id=user_id)
        return self.repository.delete(
            goal_id,
            uid
        )

    def goal_remaining(self, *args, user_id=None):
        goal = self.get_goal(*args, user_id=user_id)

        if goal is None:
            return None

        return max(
            goal.target_amount -
            goal.current_amount,
            0.0
        )

    def goal_progress(self, *args, user_id=None):
        goal = self.get_goal(*args, user_id=user_id)

        if goal is None:
            return None

        if goal.target_amount <= 0:
            return 0.0

        progress = (
            goal.current_amount /
            goal.target_amount
        ) * 100

        return min(
            progress,
            100.0
        )

    def goal_completed(self, *args, user_id=None):
        goal = self.get_goal(*args, user_id=user_id)

        if goal is None:
            return False

        return (
            goal.current_amount >=
            goal.target_amount
        )

    def add_to_goal(
        self,
        *args,
        user_id=None,
        **kwargs
    ):
        if len(args) == 3:
            # could be (uid, goal_id, amount) or (goal_id, amount, uid)
            arg0, arg1, arg2 = args
            if isinstance(arg0, int):
                goal_id, amount, uid = arg0, arg1, arg2
            else:
                uid, goal_id, amount = arg0, arg1, arg2
        elif len(args) == 2:
            goal_id, amount = args
            uid = user_id or self.user_id
        else:
            goal_id = kwargs["goal_id"]
            amount = kwargs["amount"]
            uid = user_id or kwargs.get("user_id", self.user_id)

        goal = self.get_goal(goal_id, user_id=uid)

        if goal is None:
            return False

        if float(amount) <= 0:
            return False

        goal.current_amount += float(amount)

        return self.repository.update(
            goal,
            uid
        )