from app.expense_manager import ExpenseManager


def display_menu():
    print("\n================================")
    print("      SMART EXPENSE MANAGER")
    print("================================")
    print("1. Add Expense")
    print("2. Delete Expense")
    print("3. Total Expenses")
    print("4. Category Total")
    print("5. List Expenses")
    print("6. Exit")
    print("================================")


def main():
    manager = ExpenseManager()

    while True:
        display_menu()

        choice = input("Enter choice: ")

        if choice == "1":
            print("Description:")
            description = input()

            print("Amount:")
            amount = float(input())

            print("Category:")
            category = input()

            expense = manager.add_expense(
                description,
                amount,
                category
            )

            print(f"Expense {expense.id} added successfully.")

        elif choice == "2":
            print("Enter ID to delete:")
            expense_id = int(input())

            deleted = manager.delete_expense(expense_id)

            if deleted:
                print("Expense deleted successfully.")
            else:
                print("Expense not found.")

        elif choice == "3":
            total = manager.total_expenses()
            print(f"{total:.2f}")

        elif choice == "4":
            print("Category Total selected")

        elif choice == "5":
            expenses = manager.list_expenses()

            for expense in expenses:
                print(
                    f"{expense.id} "
                    f"{expense.description} "
                    f"{expense.amount:.2f} "
                    f"{expense.category}"
                )

        elif choice == "6":
            print("Exiting Smart Expense Manager...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()