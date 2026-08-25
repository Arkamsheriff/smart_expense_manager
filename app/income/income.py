from datetime import datetime


class Income:

    def __init__(
        self,
        income_id,
        description,
        amount,
        category,
        created_at=None
    ):
        self.id = income_id
        self.description = description
        self.amount = float(amount)
        self.category = category
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return (
            f"Income("
            f"id={self.id}, "
            f"description='{self.description}', "
            f"amount={self.amount}, "
            f"category='{self.category}', "
            f"created_at={self.created_at}"
            f")"
        )