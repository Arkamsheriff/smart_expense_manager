from datetime import datetime


class Budget:
    def __init__(
        self,
        budget_id,
        month,
        amount,
        created_at=None
    ):
        self.id = budget_id
        self.month = month
        self.amount = amount
        self.created_at = created_at or datetime.now()