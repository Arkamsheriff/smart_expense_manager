from datetime import datetime


class Expense:
    def __init__(
        self,
        expense_id,
        description,
        amount,
        category,
        created_at=None
    ):
        self.id = expense_id
        self.description = description
        self.amount = amount
        self.category = category
        self.created_at = created_at or datetime.now()