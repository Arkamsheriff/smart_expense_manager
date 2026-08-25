from app.validators import (
    get_non_empty_input,
    get_positive_amount,
    get_valid_id
)


def display_income_menu():
    print()
    print("================================")
    print("         INCOME MANAGEMENT")
    print("================================")
    print("1. Add Income")
    print("2. View Income")
    print("3. View All Income")
    print("4. Update Income")
    print("5. Delete Income")
    print("6. Total Income")
    print("7. Income by Category")
    print("8. Back")
    print("================================")


def display_income(income):
    print()
    print("================================")
    print("             INCOME")
    print("================================")
    print(f"ID: {income.id}")
    print(f"Description: {income.description}")
    print(f"Amount: {income.amount:.2f}")
    print(f"Category: {income.category}")
    print(
        f"Created At: "
        f"{income.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print("================================")


def display_incomes(incomes):
    if not incomes:
        print("No income found.")
        return

    print()
    print("Income")
    print("------")

    for income in incomes:
        print(
            f"{income.id} "
            f"{income.description} "
            f"{income.amount:.2f} "
            f"{income.category} "
            f"{income.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )


def handle_income_menu(manager):
    while True:
        display_income_menu()

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

            try:
                income = manager.create_income(
                    description,
                    amount,
                    category
                )

                print(
                    f"Income {income.id} "
                    f"added successfully."
                )

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            income_id = get_valid_id(
                "Enter ID: "
            )

            income = manager.get_income(
                income_id
            )

            if income is None:
                print("Income not found.")
            else:
                display_income(income)

        elif choice == "3":
            incomes = manager.get_all_income()

            display_incomes(incomes)

        elif choice == "4":
            income_id = get_valid_id(
                "Enter ID to update: "
            )

            income = manager.get_income(
                income_id
            )

            if income is None:
                print("Income not found.")
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

            try:
                updated = manager.update_income(
                    income_id,
                    description,
                    amount,
                    category
                )

                if updated:
                    print(
                        "Income updated successfully."
                    )
                else:
                    print("Income not found.")

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":
            income_id = get_valid_id(
                "Enter ID to delete: "
            )

            deleted = manager.delete_income(
                income_id
            )

            if deleted:
                print(
                    "Income deleted successfully."
                )
            else:
                print("Income not found.")

        elif choice == "6":
            total = manager.total_income()

            print(
                f"Total Income: {total:.2f}"
            )

        elif choice == "7":
            category = get_non_empty_input(
                "Enter category: "
            )

            incomes = manager.get_income_by_category(
                category
            )

            display_incomes(incomes)

        elif choice == "8":
            break

        else:
            print("Invalid choice.")