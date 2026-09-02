import pytest


def test_dashboard_summary_empty(client):
    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["totalIncome"] == 0
    assert data["totalExpenses"] == 0
    assert data["currentBalance"] == 0
    assert data["savingsRate"] == 0

    assert data["recentExpenses"] == []
    assert data["recentIncome"] == []
    assert data["upcomingRecurring"] == []
    assert data["goals"] == []
    assert data["budgets"] == []
    assert data["expenseByCategory"] == []
    assert data["incomeVsExpenseByMonth"] == []


def test_dashboard_summary_with_income_and_expenses(client):
    income_payload = {
        "description": "Monthly Salary",
        "amount": 50000,
        "category": "Salary"
    }

    expense_payload_1 = {
        "description": "Rent",
        "amount": 15000,
        "category": "Housing"
    }

    expense_payload_2 = {
        "description": "Groceries",
        "amount": 5000,
        "category": "Food"
    }

    client.post("/api/income", json=income_payload)
    client.post("/api/expenses", json=expense_payload_1)
    client.post("/api/expenses", json=expense_payload_2)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["totalIncome"] == 50000
    assert data["totalExpenses"] == 20000
    assert data["currentBalance"] == 30000
    assert data["savingsRate"] == 60

    assert len(data["recentExpenses"]) == 2
    assert len(data["recentIncome"]) == 1


def test_dashboard_expense_by_category(client):
    expenses = [
        {
            "description": "Lunch",
            "amount": 300,
            "category": "Food"
        },
        {
            "description": "Dinner",
            "amount": 700,
            "category": "Food"
        },
        {
            "description": "Bus",
            "amount": 100,
            "category": "Transport"
        }
    ]

    for expense in expenses:
        client.post("/api/expenses", json=expense)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    category_totals = {
        item["category"]: item["total"]
        for item in data["expenseByCategory"]
    }

    assert category_totals["Food"] == 1000
    assert category_totals["Transport"] == 100


def test_dashboard_income_vs_expenses_by_month(client):
    income = {
        "description": "Salary",
        "amount": 50000,
        "category": "Salary"
    }

    expense = {
        "description": "Rent",
        "amount": 15000,
        "category": "Housing"
    }

    client.post("/api/income", json=income)
    client.post("/api/expenses", json=expense)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["incomeVsExpenseByMonth"]) >= 1

    monthly = data["incomeVsExpenseByMonth"][0]

    assert "month" in monthly
    assert "income" in monthly
    assert "expenses" in monthly


def test_dashboard_with_budget(client):
    budget_payload = {
        "category": "2026-09",
        "amount": 30000,
        "period": "monthly"
    }

    expense_payload = {
        "description": "Monthly Rent",
        "amount": 10000,
        "category": "Housing"
    }

    client.post("/api/budgets", json=budget_payload)
    client.post("/api/expenses", json=expense_payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["budgets"]) == 1

    budget = data["budgets"][0]

    assert budget["amount"] == 30000
    assert budget["spent"] == 10000
    assert budget["remaining"] == 20000
    assert budget["percentUsed"] == pytest.approx(100 / 3)


def test_dashboard_with_goal(client):
    goal_payload = {
        "name": "Emergency Fund",
        "target_amount": 100000,
        "current_amount": 25000,
        "target_date": "2027-12-31"
    }

    client.post("/api/goals", json=goal_payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["goals"]) == 1

    goal = data["goals"][0]

    assert goal["name"] == "Emergency Fund"
    assert goal["target_amount"] == 100000
    assert goal["current_amount"] == 25000
    assert goal["remaining"] == 75000
    assert goal["percentComplete"] == 25
    assert goal["target_date"] == "2027-12-31"


def test_dashboard_with_active_recurring_expense(client):
    recurring_payload = {
        "description": "Netflix",
        "amount": 649,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    client.post("/api/recurring", json=recurring_payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["upcomingRecurring"]) == 1

    recurring = data["upcomingRecurring"][0]

    assert recurring["description"] == "Netflix"
    assert recurring["amount"] == 649
    assert recurring["category"] == "Entertainment"
    assert recurring["frequency"] == "Monthly"
    assert recurring["is_active"] is True
    assert recurring["next_due_date"] == "2026-10-01"


def test_dashboard_excludes_inactive_recurring_expenses(client):
    recurring_payload = {
        "description": "Inactive Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": False
    }

    client.post("/api/recurring", json=recurring_payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["upcomingRecurring"] == []


def test_dashboard_limits_recent_expenses_to_five(client):
    for number in range(1, 8):
        payload = {
            "description": f"Expense {number}",
            "amount": number * 100,
            "category": "General"
        }

        client.post("/api/expenses", json=payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["recentExpenses"]) == 5


def test_dashboard_limits_recent_income_to_five(client):
    for number in range(1, 8):
        payload = {
            "description": f"Income {number}",
            "amount": number * 1000,
            "category": "Other"
        }

        client.post("/api/income", json=payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["recentIncome"]) == 5


def test_dashboard_limits_upcoming_recurring_to_five(client):
    for number in range(1, 8):
        payload = {
            "description": f"Subscription {number}",
            "amount": number * 100,
            "category": "Entertainment",
            "frequency": "Monthly",
            "start_date": f"2026-09-{number:02d}",
            "active": True
        }

        client.post("/api/recurring", json=payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert len(data["upcomingRecurring"]) == 5


def test_dashboard_zero_income_savings_rate(client):
    expense_payload = {
        "description": "Food",
        "amount": 1000,
        "category": "Food"
    }

    client.post("/api/expenses", json=expense_payload)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["totalIncome"] == 0
    assert data["totalExpenses"] == 1000
    assert data["currentBalance"] == -1000
    assert data["savingsRate"] == 0