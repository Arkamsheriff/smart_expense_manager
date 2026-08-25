from app.expense_manager import ExpenseManager
from app.budget.budget_manager import BudgetManager
from app.budget.budget_cli import handle_budget_menu
from app.goals.goal_manager import GoalManager
from app.goals.goal_cli import handle_goal_menu
from app.recurring.recurring_manager import RecurringExpenseManager
from app.recurring.recurring_cli import handle_recurring_menu
from app.income.income_manager import IncomeManager
from app.income.income_cli import handle_income_menu
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
    print("9. Search & Filter")
    print("10. Budget Management")
    print("11. Financial Goals")
    print("12. Recurring Expenses")
    print("13. Income Management")
    print("14. Exit")
    print("================================")

def handle_charts(report_service, visualization_service, show_charts=True):
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

def handle_reports(report_service, visualization_service, show_charts=True):
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
            handle_charts(
                report_service,
                visualization_service,
                show_charts
            )

        elif report_choice == "8":
            break

        else:
            print("Invalid choice.")

def handle_export(manager, csv_exporter):
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

def handle_search_filter(manager):
    while True:
        print()
        print("================================")
        print("        SEARCH & FILTER")
        print("================================")
        print("1. Search by Description")
        print("2. Filter by Category")
        print("3. Filter by Amount Range")
        print("4. Back")
        print("================================")

        search_choice = input("Enter choice: ")

        if search_choice == "1":
            keyword = get_non_empty_input(
                "Enter description keyword: "
            )

            expenses = manager.search_expenses(keyword)

            if not expenses:
                print("No expenses found.")
            else:
                for expense in expenses:
                    print(
                        f"{expense.id} "
                        f"{expense.description} "
                        f"{expense.amount:.2f} "
                        f"{expense.category} "
                        f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

        elif search_choice == "2":
            category = get_non_empty_input(
                "Enter category: "
            )

            expenses = manager.filter_expenses_by_category(
                category
            )

            if not expenses:
                print("No expenses found.")
            else:
                for expense in expenses:
                    print(
                        f"{expense.id} "
                        f"{expense.description} "
                        f"{expense.amount:.2f} "
                        f"{expense.category} "
                        f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

        elif search_choice == "3":
            minimum = get_positive_amount(
                "Enter minimum amount: "
            )

            maximum = get_positive_amount(
                "Enter maximum amount: "
            )

            if minimum > maximum:
                print(
                    "Minimum amount cannot exceed maximum amount."
                )
                continue

            expenses = manager.filter_expenses_by_amount(
                minimum,
                maximum
            )

            if not expenses:
                print("No expenses found.")
            else:
                for expense in expenses:
                    print(
                        f"{expense.id} "
                        f"{expense.description} "
                        f"{expense.amount:.2f} "
                        f"{expense.category} "
                        f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

        elif search_choice == "4":
            break

        else:
            print("Invalid choice.")

def main(show_charts=True):
    initialize_database()
    manager = ExpenseManager()
    budget_manager = BudgetManager()
    goal_manager = GoalManager()
    recurring_manager = RecurringExpenseManager()
    income_manager = IncomeManager()
    report_service = ReportService(manager)
    visualization_service = VisualizationService()
    csv_exporter = CSVExporter()
    

    while True:
        display_menu()
        def handle_add_expense(manager):
            description = get_non_empty_input("Description: ")
            amount = get_positive_amount("Amount: ")
            category = get_non_empty_input("Category: ")

            expense = manager.add_expense(
                description,
                amount,
                category
            )

            print(f"Expense {expense.id} added successfully.")


        def handle_delete_expense(manager):
            expense_id = get_valid_id("Enter ID to delete: ")

            deleted = manager.delete_expense(expense_id)

            if deleted:
                print("Expense deleted successfully.")
            else:
                print("Expense not found.")


        def handle_total_expenses(manager):
            total = manager.total_expenses()
            print(f"{total:.2f}")


        def handle_category_total(manager):
            category = get_non_empty_input("Enter category: ")
            total = manager.category_total(category)
            print(f"{total:.2f}")


        def handle_list_expenses(manager):
            expenses = manager.list_expenses()

            for expense in expenses:
                print(
                    f"{expense.id} "
                    f"{expense.description} "
                    f"{expense.amount:.2f} "
                    f"{expense.category} "
                    f"{expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )

        def handle_update_expense(manager):
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

        choice = input("Enter choice: ")

        if choice == "1":
            handle_add_expense(manager)
        elif choice == "2":
            handle_delete_expense(manager)
        elif choice == "3":
             handle_total_expenses(manager)

        elif choice == "4":
            handle_category_total(manager)

        elif choice == "5":
            handle_list_expenses(manager)
        elif choice == "6":
            handle_update_expense(manager)
        elif choice == "7":
            handle_reports(
                report_service,
                visualization_service,
                show_charts
            )
        elif choice == "8":
            handle_export(manager, csv_exporter)
        elif choice == "9":
            handle_search_filter(manager)
        elif choice == "10":
            handle_budget_menu(
                budget_manager,
                manager
            )
        elif choice == "11":
            handle_goal_menu(
                goal_manager
            )
        elif choice == "12":
            handle_recurring_menu(
                recurring_manager
            )
        elif choice == "13":
            handle_income_menu(
                income_manager
            )
        elif choice == "14":
            print("Exiting Smart Expense Manager...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
