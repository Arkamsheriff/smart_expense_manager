def test_get_recurring_expenses_empty(client):
    response = client.get("/api/recurring")

    assert response.status_code == 200
    assert response.json() == []


def test_create_recurring_expense(client):
    payload = {
        "description": "Netflix Subscription",
        "amount": 649,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "end_date": "2027-09-01",
        "active": True
    }

    response = client.post("/api/recurring", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["description"] == "Netflix Subscription"
    assert data["amount"] == 649
    assert data["category"] == "Entertainment"
    assert data["frequency"] == "Monthly"
    assert data["start_date"] == "2026-09-01"
    assert data["end_date"] == "2027-09-01"
    assert data["active"] is True


def test_get_recurring_expense_by_id(client):
    payload = {
        "description": "Internet Bill",
        "amount": 999,
        "category": "Utilities",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    create_response = client.post("/api/recurring", json=payload)
    expense_id = create_response.json()["id"]

    response = client.get(f"/api/recurring/{expense_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["description"] == "Internet Bill"
    assert data["amount"] == 999
    assert data["frequency"] == "Monthly"


def test_get_recurring_expense_not_found(client):
    response = client.get("/api/recurring/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recurring expense not found"


def test_get_all_recurring_expenses(client):
    payload_1 = {
        "description": "Netflix",
        "amount": 649,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    payload_2 = {
        "description": "Gym Membership",
        "amount": 1500,
        "category": "Health",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    client.post("/api/recurring", json=payload_1)
    client.post("/api/recurring", json=payload_2)

    response = client.get("/api/recurring")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["description"] == "Netflix"
    assert data[1]["description"] == "Gym Membership"


def test_update_recurring_expense(client):
    create_payload = {
        "description": "Old Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    create_response = client.post(
        "/api/recurring",
        json=create_payload
    )

    expense_id = create_response.json()["id"]

    update_payload = {
        "description": "Updated Subscription",
        "amount": 750,
        "category": "Utilities",
        "frequency": "Weekly",
        "start_date": "2026-09-05",
        "end_date": "2027-09-05",
        "active": False
    }

    response = client.put(
        f"/api/recurring/{expense_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["description"] == "Updated Subscription"
    assert data["amount"] == 750
    assert data["category"] == "Utilities"
    assert data["frequency"] == "Weekly"
    assert data["start_date"] == "2026-09-05"
    assert data["end_date"] == "2027-09-05"
    assert data["active"] is False


def test_update_recurring_expense_not_found(client):
    payload = {
        "description": "Test Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    response = client.put(
        "/api/recurring/9999",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recurring expense not found"


def test_delete_recurring_expense(client):
    payload = {
        "description": "Temporary Subscription",
        "amount": 300,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    create_response = client.post(
        "/api/recurring",
        json=payload
    )

    expense_id = create_response.json()["id"]

    response = client.delete(
        f"/api/recurring/{expense_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Recurring expense deleted successfully"
    )

    get_response = client.get(
        f"/api/recurring/{expense_id}"
    )

    assert get_response.status_code == 404


def test_delete_recurring_expense_not_found(client):
    response = client.delete("/api/recurring/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recurring expense not found"


def test_toggle_recurring_expense(client):
    payload = {
        "description": "Cloud Storage",
        "amount": 200,
        "category": "Technology",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    create_response = client.post(
        "/api/recurring",
        json=payload
    )

    expense_id = create_response.json()["id"]

    response = client.patch(
        f"/api/recurring/{expense_id}/toggle"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["active"] is False

    # Toggle again
    response = client.patch(
        f"/api/recurring/{expense_id}/toggle"
    )

    assert response.status_code == 200
    assert response.json()["active"] is True


def test_toggle_recurring_expense_not_found(client):
    response = client.patch(
        "/api/recurring/9999/toggle"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recurring expense not found"


def test_get_next_due_date(client):
    payload = {
        "description": "Monthly Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-15",
        "active": True
    }

    create_response = client.post(
        "/api/recurring",
        json=payload
    )

    expense_id = create_response.json()["id"]

    response = client.get(
        f"/api/recurring/{expense_id}/next-due"
    )

    assert response.status_code == 200
    assert response.json() == "2026-10-15"


def test_get_next_due_date_inactive(client):
    payload = {
        "description": "Inactive Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-15",
        "active": False
    }

    create_response = client.post(
        "/api/recurring",
        json=payload
    )

    expense_id = create_response.json()["id"]

    response = client.get(
        f"/api/recurring/{expense_id}/next-due"
    )

    assert response.status_code == 200
    assert response.json() is None


def test_get_next_due_date_not_found(client):
    response = client.get(
        "/api/recurring/9999/next-due"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recurring expense not found"


def test_create_invalid_frequency(client):
    payload = {
        "description": "Invalid Subscription",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Hourly",
        "start_date": "2026-09-01",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid frequency."


def test_create_negative_amount(client):
    payload = {
        "description": "Invalid Expense",
        "amount": -100,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Amount cannot be negative."


def test_create_invalid_start_date(client):
    payload = {
        "description": "Invalid Date",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "01-09-2026",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Date must use YYYY-MM-DD format."
    )


def test_create_end_date_before_start_date(client):
    payload = {
        "description": "Invalid Date Range",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-15",
        "end_date": "2026-09-01",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "End date cannot be before start date."
    )


def test_create_empty_description(client):
    payload = {
        "description": "   ",
        "amount": 500,
        "category": "Entertainment",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Description cannot be empty."
    )


def test_create_empty_category(client):
    payload = {
        "description": "Subscription",
        "amount": 500,
        "category": "   ",
        "frequency": "Monthly",
        "start_date": "2026-09-01",
        "active": True
    }

    response = client.post(
        "/api/recurring",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Category cannot be empty."
    )