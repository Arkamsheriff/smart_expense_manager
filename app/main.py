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
    while True:
        display_menu()

        choice = input("Enter choice: ")

        if choice == "1":
            print("Add Expense selected")

        elif choice == "2":
            print("Delete Expense selected")

        elif choice == "3":
            print("Total Expenses selected")

        elif choice == "4":
            print("Category Total selected")

        elif choice == "5":
            print("List Expenses selected")

        elif choice == "6":
            print("Exiting Smart Expense Manager...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()