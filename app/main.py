from app.expense_manager import ExpenseManager
from app.database.repository import initialize_database
from app.validators import (
    get_non_empty_input,
    get_positive_amount,
    get_valid_id
)

def display_menu():
    print("\n================================")
    print("      SMART EXPENSE MANAGER")
    print("================================")
    print("1. Add Expense")
    print("2. Delete Expense")
    print("3. Total Expenses")
    print("4. Category Total")
    print("5. List Expenses")
    print("6. Update Expense")
    print("7. Exit")
    print("================================")


def main():
    initialize_database()
    manager = ExpenseManager()

    while True:
        display_menu()

        choice = input("Enter choice: ")

        if choice == "1":
            description = get_non_empty_input("Description: ")
            amount = get_positive_amount("Amount: ")
            category = get_non_empty_input("Category: ")
            expense = manager.add_expense(
                description,
                amount,
                category
            )
            print(f"Expense {expense.id} added successfully.")

        elif choice == "2":
            expense_id = get_valid_id("Enter ID to delete: ")

            deleted = manager.delete_expense(expense_id)

            if deleted:
                print("Expense deleted successfully.")
            else:
                print("Expense not found.")

        elif choice == "3":
            total = manager.total_expenses()
            print(f"{total:.2f}")

        elif choice == "4":
            category = get_non_empty_input("Enter category: ")
            total = manager.category_total(category)
            print(f"{total:.2f}")

        elif choice == "5":
            expenses = manager.list_expenses()

            for expense in expenses:
                print(
                    f"{expense.id} "
                    f"{expense.description} "
                    f"{expense.amount:.2f} "
                    f"{expense.category} "
                    f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )

        elif choice == "6":
            expense_id = get_valid_id("Enter ID to update: ")
            description = get_non_empty_input("New Description: ")
            amount = get_positive_amount("New Amount: ")
            category = get_non_empty_input("New Category: ")
            updated = manager.update_expense(
                expense_id,
                description,
                amount,
                category
            )
            if updated:
                print("Expense updated successfully.")
            else:
                print("Expense not found.")
        elif choice == "7":
            print("Exiting Smart Expense Manager...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()