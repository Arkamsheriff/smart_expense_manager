class RecurringExpense:
    def __init__(
        self,
        expense_id,
        description,
        amount,
        category,
        frequency,
        start_date,
        end_date=None,
        active=True
    ):
        self.id = expense_id
        self.description = description
        self.amount = amount
        self.category = category
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.active = active