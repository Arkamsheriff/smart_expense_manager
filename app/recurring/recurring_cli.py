from datetime import datetime

from app.validators import (
    get_non_empty_input,
    get_positive_amount,
    get_valid_id
)


def display_recurring_menu():
    print()
    print("================================")
    print("       RECURRING EXPENSES")
    print("================================")
    print("1. Create Recurring Expense")
    print("2. View Recurring Expense")
    print("3. View All Recurring Expenses")
    print("4. Update Recurring Expense")
    print("5. Delete Recurring Expense")
    print("6. Activate/Deactivate")
    print("7. Next Due Date")
    print("8. Back")
    print("================================")


def get_frequency():
    while True:
        print()
        print("Frequency:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        print("4. Yearly")

        choice = input("Enter frequency: ").strip()

        frequencies = {
            "1": "Daily",
            "2": "Weekly",
            "3": "Monthly",
            "4": "Yearly"
        }

        if choice in frequencies:
            return frequencies[choice]

        print("Invalid frequency.")


def get_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def get_optional_date(prompt):
    while True:
        value = input(prompt).strip()

        if not value:
            return None

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def display_recurring_expense(expense):
    print()
    print("================================")
    print("     RECURRING EXPENSE")
    print("================================")
    print(f"ID: {expense.id}")
    print(f"Description: {expense.description}")
    print(f"Amount: {expense.amount:.2f}")
    print(f"Category: {expense.category}")
    print(f"Frequency: {expense.frequency}")
    print(f"Start Date: {expense.start_date}")
    print(
        f"End Date: "
        f"{expense.end_date or 'No end date'}"
    )
    print(
        f"Status: "
        f"{'Active' if expense.active else 'Inactive'}"
    )
    print("================================")


def display_recurring_expenses(expenses):
    if not expenses:
        print("No recurring expenses found.")
        return

    print()
    print("Recurring Expenses")
    print("-------------------")

    for expense in expenses:
        print(
            f"{expense.id} "
            f"{expense.description} "
            f"{expense.amount:.2f} "
            f"{expense.category} "
            f"{expense.frequency} "
            f"{'Active' if expense.active else 'Inactive'}"
        )


def handle_recurring_menu(manager):
    while True:
        display_recurring_menu()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            description = get_non_empty_input(
                "Description: "
            )

            amount = get_positive_amount(
                "Amount: "
            )

            category = get_non_empty_input(
                "Category: "
            )

            frequency = get_frequency()

            start_date = get_date(
                "Start date (YYYY-MM-DD): "
            )

            end_date = get_optional_date(
                "End date (YYYY-MM-DD, blank for none): "
            )

            try:
                expense = manager.create_recurring_expense(
                    description,
                    amount,
                    category,
                    frequency,
                    start_date,
                    end_date
                )

                print(
                    f"Recurring expense "
                    f"{expense.id} created successfully."
                )

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            expense_id = get_valid_id(
                "Enter ID: "
            )

            expense = manager.get_recurring_expense(
                expense_id
            )

            if expense is None:
                print("Recurring expense not found.")
            else:
                display_recurring_expense(expense)

        elif choice == "3":
            expenses = manager.get_all_recurring_expenses()

            display_recurring_expenses(expenses)

        elif choice == "4":
            expense_id = get_valid_id(
                "Enter ID to update: "
            )

            expense = manager.get_recurring_expense(
                expense_id
            )

            if expense is None:
                print("Recurring expense not found.")
                continue

            description = get_non_empty_input(
                "New description: "
            )

            amount = get_positive_amount(
                "New amount: "
            )

            category = get_non_empty_input(
                "New category: "
            )

            frequency = get_frequency()

            start_date = get_date(
                "New start date (YYYY-MM-DD): "
            )

            end_date = get_optional_date(
                "New end date (YYYY-MM-DD, blank for none): "
            )

            try:
                updated = manager.update_recurring_expense(
                    expense_id,
                    description,
                    amount,
                    category,
                    frequency,
                    start_date,
                    end_date,
                    expense.active
                )

                if updated:
                    print(
                        "Recurring expense updated successfully."
                    )
                else:
                    print("Recurring expense not found.")

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":
            expense_id = get_valid_id(
                "Enter ID to delete: "
            )

            deleted = manager.delete_recurring_expense(
                expense_id
            )

            if deleted:
                print(
                    "Recurring expense deleted successfully."
                )
            else:
                print("Recurring expense not found.")

        elif choice == "6":
            expense_id = get_valid_id(
                "Enter ID: "
            )

            expense = manager.get_recurring_expense(
                expense_id
            )

            if expense is None:
                print("Recurring expense not found.")
                continue

            updated = manager.toggle_active(
                expense_id
            )

            if updated:
                status = (
                    "activated"
                    if not expense.active
                    else "deactivated"
                )

                print(
                    f"Recurring expense {status} successfully."
                )
            else:
                print("Unable to change status.")

        elif choice == "7":
            expense_id = get_valid_id(
                "Enter ID: "
            )

            expense = manager.get_recurring_expense(
                expense_id
            )

            if expense is None:
                print("Recurring expense not found.")
                continue

            next_due = manager.get_next_due_date(
                expense_id
            )

            if next_due is None:
                print(
                    "No next due date available."
                )
            else:
                print(
                    f"Next due date: {next_due}"
                )

        elif choice == "8":
            break

        else:
            print("Invalid choice.")