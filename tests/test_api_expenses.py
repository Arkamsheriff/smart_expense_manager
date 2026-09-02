def test_get_expenses_empty(client):
    response = client.get("/api/expenses")

    assert response.status_code == 200
    assert response.json() == []


def test_create_expense(client):
    response = client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["description"] == "Lunch"
    assert data["amount"] == 250
    assert data["category"] == "Food"
    assert "created_at" in data


def test_get_expense(client):
    create_response = client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    response = client.get(f"/api/expenses/{expense_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["description"] == "Lunch"
    assert data["amount"] == 250
    assert data["category"] == "Food"


def test_get_expense_not_found(client):
    response = client.get("/api/expenses/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_update_expense(client):
    create_response = client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    response = client.put(
        f"/api/expenses/{expense_id}",
        json={
            "description": "Dinner",
            "amount": 500,
            "category": "Food",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["description"] == "Dinner"
    assert data["amount"] == 500
    assert data["category"] == "Food"


def test_update_expense_not_found(client):
    response = client.put(
        "/api/expenses/99999",
        json={
            "description": "Dinner",
            "amount": 500,
            "category": "Food",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_delete_expense(client):
    create_response = client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    response = client.delete(f"/api/expenses/{expense_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Expense deleted successfully"

    get_response = client.get(f"/api/expenses/{expense_id}")

    assert get_response.status_code == 404


def test_delete_expense_not_found(client):
    response = client.delete("/api/expenses/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_get_total_expenses(client):
    client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Taxi",
            "amount": 150,
            "category": "Transport",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Dinner",
            "amount": 400,
            "category": "Food",
        },
    )

    response = client.get("/api/expenses/total/summary")

    assert response.status_code == 200
    assert response.json()["total"] == 800


def test_get_category_total(client):
    client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Dinner",
            "amount": 400,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Taxi",
            "amount": 150,
            "category": "Transport",
        },
    )

    response = client.get("/api/expenses/category/Food")

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "Food"
    assert data["total"] == 650


def test_search_expenses(client):
    client.post(
        "/api/expenses",
        json={
            "description": "Lunch at restaurant",
            "amount": 250,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Taxi to office",
            "amount": 150,
            "category": "Transport",
        },
    )

    response = client.get("/api/expenses/search/Lunch")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["description"] == "Lunch at restaurant"


def test_filter_by_category(client):
    client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Taxi",
            "amount": 150,
            "category": "Transport",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Dinner",
            "amount": 400,
            "category": "Food",
        },
    )

    response = client.get("/api/expenses/filter/category/Food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    categories = [expense["category"] for expense in data]

    assert all(category == "Food" for category in categories)


def test_filter_by_amount(client):
    client.post(
        "/api/expenses",
        json={
            "description": "Coffee",
            "amount": 100,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    client.post(
        "/api/expenses",
        json={
            "description": "Shopping",
            "amount": 1000,
            "category": "Shopping",
        },
    )

    response = client.get(
        "/api/expenses/filter/amount",
        params={
            "minimum": 200,
            "maximum": 500,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["description"] == "Lunch"
    assert data[0]["amount"] == 250


def test_filter_by_amount_negative_values(client):
    response = client.get(
        "/api/expenses/filter/amount",
        params={
            "minimum": -100,
            "maximum": 500,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Amounts cannot be negative"


def test_filter_by_amount_minimum_greater_than_maximum(client):
    response = client.get(
        "/api/expenses/filter/amount",
        params={
            "minimum": 500,
            "maximum": 200,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Minimum amount cannot exceed maximum amount"
    )


def test_create_expense_validation(client):
    response = client.post(
        "/api/expenses",
        json={
            "description": "",
            "amount": 250,
            "category": "Food",
        },
    )

    assert response.status_code == 422


def test_create_expense_invalid_amount(client):
    response = client.post(
        "/api/expenses",
        json={
            "description": "Lunch",
            "amount": 0,
            "category": "Food",
        },
    )

    assert response.status_code == 422