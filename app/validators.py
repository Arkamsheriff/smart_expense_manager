def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty.")


def get_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_valid_id(prompt):
    while True:
        try:
            expense_id = int(input(prompt))

            if expense_id > 0:
                return expense_id

            print("ID must be greater than 0.")

        except ValueError:
            print("Please enter a valid ID.")