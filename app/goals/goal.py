from datetime import datetime


class Goal:
    def __init__(
        self,
        goal_id,
        name,
        target_amount,
        current_amount=0.0,
        target_date=None,
        created_at=None
    ):
        self.id = goal_id
        self.name = name
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.target_date = target_date
        self.created_at = created_at or datetime.now()