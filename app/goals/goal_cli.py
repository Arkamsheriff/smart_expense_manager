from app.goals.goal_manager import GoalManager


def display_goal_menu():
    print()
    print("================================")
    print("          GOAL MANAGEMENT")
    print("================================")
    print("1. Create Goal")
    print("2. View Goal")
    print("3. View All Goals")
    print("4. Update Goal")
    print("5. Add Money to Goal")
    print("6. Goal Progress")
    print("7. Goal Status")
    print("8. Delete Goal")
    print("9. Back")
    print("================================")


def get_goal_id():
    while True:
        value = input("Enter goal ID: ").strip()

        try:
            goal_id = int(value)

            if goal_id > 0:
                return goal_id

        except ValueError:
            pass

        print("Invalid goal ID. Please enter a positive integer.")


def get_goal_name():
    while True:
        name = input("Enter goal name: ").strip()

        if name:
            return name

        print("Goal name cannot be empty.")


def get_amount(prompt):
    while True:
        value = input(prompt).strip()

        try:
            amount = float(value)

            if amount >= 0:
                return amount

        except ValueError:
            pass

        print("Invalid amount. Please enter a non-negative number.")


def get_positive_amount(prompt):
    while True:
        value = input(prompt).strip()

        try:
            amount = float(value)

            if amount > 0:
                return amount

        except ValueError:
            pass

        print("Invalid amount. Please enter a positive number.")


def get_target_date():
    while True:
        target_date = input(
            "Enter target date (YYYY-MM) or leave blank: "
        ).strip()

        if not target_date:
            return None

        if (
            len(target_date) == 7
            and target_date[4] == "-"
        ):
            year, month = target_date.split("-")

            if (
                year.isdigit()
                and month.isdigit()
                and 1 <= int(month) <= 12
            ):
                return target_date

        print("Invalid date. Please use YYYY-MM.")


def display_goal(goal):
    print()
    print("================================")
    print("             GOAL")
    print("================================")
    print(f"ID: {goal.id}")
    print(f"Name: {goal.name}")
    print(f"Target Amount: {goal.target_amount:.2f}")
    print(f"Current Amount: {goal.current_amount:.2f}")

    if goal.target_date:
        print(f"Target Date: {goal.target_date}")
    else:
        print("Target Date: Not set")

    print("================================")


def display_progress(goal, progress, remaining):
    print()
    print("================================")
    print("          GOAL PROGRESS")
    print("================================")
    print(f"Goal: {goal.name}")
    print(f"Target: {goal.target_amount:.2f}")
    print(f"Saved: {goal.current_amount:.2f}")
    print(f"Remaining: {remaining:.2f}")
    print(f"Progress: {progress:.2f}%")

    if progress >= 100:
        print("Status: GOAL COMPLETED")
    else:
        print("Status: IN PROGRESS")

    print("================================")


def handle_goal_menu(goal_manager):
    while True:
        display_goal_menu()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = get_goal_name()

            target_amount = get_amount(
                "Enter target amount: "
            )

            current_amount = get_amount(
                "Enter current amount: "
            )

            target_date = get_target_date()

            goal = goal_manager.create_goal(
                name,
                target_amount,
                current_amount,
                target_date
            )

            print(
                f"Goal {goal.id} created successfully."
            )

        elif choice == "2":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
            else:
                display_goal(goal)

        elif choice == "3":
            goals = goal_manager.get_all_goals()

            if not goals:
                print("No goals found.")
            else:
                print()
                print("================================")
                print("            ALL GOALS")
                print("================================")

                for goal in goals:
                    progress = goal_manager.goal_progress(
                        goal.id
                    )

                    print(
                        f"{goal.id}. "
                        f"{goal.name} - "
                        f"{goal.current_amount:.2f}/"
                        f"{goal.target_amount:.2f} "
                        f"({progress:.2f}%)"
                    )

                print("================================")

        elif choice == "4":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
                continue

            name = get_goal_name()

            target_amount = get_amount(
                "Enter target amount: "
            )

            current_amount = get_amount(
                "Enter current amount: "
            )

            target_date = get_target_date()

            updated = goal_manager.update_goal(
                goal_id,
                name,
                target_amount,
                current_amount,
                target_date
            )

            if updated:
                print("Goal updated successfully.")
            else:
                print("Goal could not be updated.")

        elif choice == "5":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
                continue

            amount = get_positive_amount(
                "Enter amount to add: "
            )

            added = goal_manager.add_to_goal(
                goal_id,
                amount
            )

            if added:
                print(
                    f"{amount:.2f} added to "
                    f"{goal.name} successfully."
                )
            else:
                print("Amount could not be added.")

        elif choice == "6":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
                continue

            progress = goal_manager.goal_progress(
                goal_id
            )

            remaining = goal_manager.goal_remaining(
                goal_id
            )

            display_progress(
                goal,
                progress,
                remaining
            )

        elif choice == "7":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
                continue

            if goal_manager.goal_completed(goal_id):
                print(
                    f"Goal '{goal.name}' "
                    "has been completed."
                )
            else:
                remaining = goal_manager.goal_remaining(
                    goal_id
                )

                print(
                    f"Goal '{goal.name}' "
                    f"is still in progress."
                )
                print(
                    f"Amount remaining: "
                    f"{remaining:.2f}"
                )

        elif choice == "8":
            goal_id = get_goal_id()

            goal = goal_manager.get_goal(goal_id)

            if goal is None:
                print("Goal not found.")
                continue

            deleted = goal_manager.delete_goal(
                goal_id
            )

            if deleted:
                print("Goal deleted successfully.")
            else:
                print("Goal could not be deleted.")

        elif choice == "9":
            break

        else:
            print("Invalid choice.")