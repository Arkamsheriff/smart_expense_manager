from app.budget.budget_manager import BudgetManager


def display_budget_menu():
    print()
    print("================================")
    print("       BUDGET MANAGEMENT")
    print("================================")
    print("1. Set Monthly Budget")
    print("2. View Monthly Budget")
    print("3. Budget Status")
    print("4. View All Budgets")
    print("5. Delete Budget")
    print("6. Back")
    print("================================")


def get_month():
    while True:
        month = input("Enter month (YYYY-MM): ").strip()

        if len(month) == 7 and month[4] == "-":
            year, month_number = month.split("-")

            if year.isdigit() and month_number.isdigit():
                month_value = int(month_number)

                if 1 <= month_value <= 12:
                    return f"{year}-{month_number}"

        print("Invalid month. Please use YYYY-MM.")


def get_budget_amount():
    while True:
        value = input("Enter budget amount: ").strip()

        try:
            amount = float(value)

            if amount >= 0:
                return amount

        except ValueError:
            pass

        print("Invalid amount. Please enter a non-negative number.")


def display_budget_status(
    budget,
    total_expenses,
    remaining,
    utilization
):
    print()
    print("================================")
    print("         BUDGET STATUS")
    print("================================")
    print(f"Month: {budget.month}")
    print(f"Budget: {budget.amount:.2f}")
    print(f"Spent: {total_expenses:.2f}")
    print(f"Remaining: {remaining:.2f}")
    print(f"Utilization: {utilization:.2f}%")

    if total_expenses > budget.amount:
        print("Status: BUDGET EXCEEDED")
    else:
        print("Status: Within Budget")

    print("================================")


def handle_budget_menu(
    budget_manager,
    expense_manager
):
    while True:
        display_budget_menu()

        choice = input("Enter choice: ")

        if choice == "1":
            month = get_month()
            amount = get_budget_amount()

            budget = budget_manager.set_budget(
                month,
                amount
            )

            print(
                f"Budget for {budget.month} "
                f"set successfully."
            )

        elif choice == "2":
            month = get_month()

            budget = budget_manager.get_budget(month)

            if budget is None:
                print("No budget found for this month.")
            else:
                print()
                print(f"Month: {budget.month}")
                print(f"Monthly Budget: {budget.amount:.2f}")

        elif choice == "3":
            month = get_month()

            budget = budget_manager.get_budget(month)

            if budget is None:
                print("No budget found for this month.")
                continue

            total_expenses = sum(
                expense.amount
                for expense in expense_manager.list_expenses()
                if expense.created_at.strftime("%Y-%m") == month
            )

            remaining = budget_manager.budget_remaining(
                month,
                total_expenses
            )

            utilization = budget_manager.budget_utilization(
                month,
                total_expenses
            )

            display_budget_status(
                budget,
                total_expenses,
                remaining,
                utilization
            )

        elif choice == "4":
            budgets = budget_manager.get_all_budgets()

            if not budgets:
                print("No budgets found.")
            else:
                print()
                print("All Budgets")
                print("-----------")

                for budget in budgets:
                    print(
                        f"{budget.month} "
                        f"{budget.amount:.2f}"
                    )

        elif choice == "5":
            month = get_month()

            budget = budget_manager.get_budget(month)

            if budget is None:
                print("No budget found for this month.")
                continue

            deleted = budget_manager.delete_budget(
                budget.id
            )

            if deleted:
                print("Budget deleted successfully.")
            else:
                print("Budget could not be deleted.")

        elif choice == "6":
            break

        else:
            print("Invalid choice.")