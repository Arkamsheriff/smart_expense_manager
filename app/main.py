from app.expense_manager import ExpenseManager
from app.database.repository import initialize_database
from app.reports.report_service import ReportService
from app.reports.visualization import VisualizationService
from app.exports.csv_exporter import CSVExporter
import matplotlib.pyplot as plt
import os
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
    print("8. Export")
    print("9. Exit")
    print("================================")


def main(show_charts=True):
    initialize_database()
    manager = ExpenseManager()
    report_service = ReportService(manager)
    visualization_service = VisualizationService()
    csv_exporter = CSVExporter()

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
                print("5. Category Summary")
                print("6. Spending Statistics")
                print("7. Charts")
                print("8. Back")
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
                    expenses = report_service.this_month()
                    summary = report_service.category_summary(expenses)
                    if not summary:
                        print("No expenses found this month.")
                    else:
                        print("Category Summary")
                        print("----------------")
                        for category, total in summary.items():
                            print(f"{category} {total:.2f}")
                elif report_choice == "6":
                    expenses = report_service.this_month()
                    statistics = report_service.spending_statistics(expenses)
                    if statistics["count"] == 0:
                        print("No expenses found this month.")
                    else:
                        print("Spending Statistics")
                        print("--------------------")
                        print(f"Number of Expenses: {statistics['count']}")
                        print(f"Total Spending: {statistics['total']:.2f}")
                        print(f"Average Expense: {statistics['average']:.2f}")
                        print(f"Highest Expense: {statistics['highest']:.2f}")
                        print(f"Lowest Expense: {statistics['lowest']:.2f}")
                elif report_choice == "7":
                    while True:
                        print()
                        print("================================")
                        print("            CHARTS")
                        print("================================")
                        print("1. Category Bar Chart")
                        print("2. Category Pie Chart")
                        print("3. Back")
                        print("================================")
                        chart_choice = input("Enter choice: ")
                        if chart_choice == "1":
                            expenses = report_service.this_month()
                            summary = report_service.category_summary(expenses)

                            figure = visualization_service.category_bar_chart(summary)

                            if figure:
                                if show_charts:
                                    plt.show()
                                plt.close(figure)

                        elif chart_choice == "2":
                            expenses = report_service.this_month()
                            summary = report_service.category_summary(expenses)

                            figure = visualization_service.category_pie_chart(summary)

                            if figure:
                                if show_charts:
                                    plt.show()
                                plt.close(figure)

                        elif chart_choice == "3":
                            break

                        else:
                            print("Invalid choice.")
                elif report_choice == "8":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "8":
            while True:
                print()
                print("================================")
                print("            EXPORT")
                print("================================")
                print("1. Export All Expenses to CSV")
                print("2. Back")
                print("================================")
                export_choice = input("Enter choice: ")
                if export_choice == "1":
                    expenses = manager.list_expenses()
                    os.makedirs("reports", exist_ok=True)
                    file_path = "reports/expenses.csv"
                    csv_exporter.export(
                        expenses,
                        file_path
                            )

                    print(
                        f"Expenses exported successfully to {file_path}"
                    )

                elif export_choice == "2":
                    break

                else:
                    print("Invalid choice.")
        elif choice == "9":
            print("Exiting Smart Expense Manager...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()