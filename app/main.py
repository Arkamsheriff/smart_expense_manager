from app.expense_manager import ExpenseManager
from app.database.repository import initialize_database
from app.reports.report_service import ReportService
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
    print("7. Reports")
    print("8. Exit")
    print("================================")


def main():
    initialize_database()
    manager = ExpenseManager()
    report_service = ReportService(manager)

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
            while True:
                print()
                print("================================")
                print("           REPORTS")
                print("================================")
                print("1. Today's Expenses")
                print("2. Today's Total")
                print("3. This Week")
                print("4. This Month")
                print("5. Back")
                print("================================")

                report_choice = input("Enter choice: ")

                if report_choice == "1":
                    expenses = report_service.today()

                    if not expenses:
                        print("No expenses found for today.")
                    else:
                        for expense in expenses:
                            print(
                                f"{expense.id} "
                                f"{expense.description} "
                                f"{expense.amount:.2f} "
                                f"{expense.category} "
                                f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                            )

                elif report_choice == "2":
                    expenses = report_service.today()

                    total = report_service.total_for_expenses(expenses)

                    print(f"{total:.2f}")

                elif report_choice == "3":
                    expenses = report_service.this_week()

                    if not expenses:
                        print("No expenses found this week.")
                    else:
                        for expense in expenses:
                            print(
                                f"{expense.id} "
                                f"{expense.description} "
                                f"{expense.amount:.2f} "
                                f"{expense.category} "
                                f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                            )

                elif report_choice == "4":
                    expenses = report_service.this_month()

                    if not expenses:
                        print("No expenses found this month.")
                    else:
                        for expense in expenses:
                            print(
                                f"{expense.id} "
                                f"{expense.description} "
                                f"{expense.amount:.2f} "
                                f"{expense.category} "
                                f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                            )

                elif report_choice == "5":
                    break

                else:
                    print("Invalid choice.")
        elif choice == "8":
            print("Exiting Smart Expense Manager...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()