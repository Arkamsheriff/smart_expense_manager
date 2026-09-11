def test_get_income_empty(client, test_db):
    response = client.get("/api/income")

    assert response.status_code == 200
    assert response.json() == []


def test_create_income(client, test_db):
    response = client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["description"] == "Monthly Salary"
    assert data["amount"] == 50000
    assert data["category"] == "Salary"
    assert "created_at" in data


def test_get_income_by_id(client, test_db):
    create_response = client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    response = client.get(
        f"/api/income/{income_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == income_id
    assert data["description"] == "Monthly Salary"
    assert data["amount"] == 50000
    assert data["category"] == "Salary"


def test_get_income_not_found(client, test_db):
    response = client.get(
        "/api/income/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Income not found"


def test_update_income(client, test_db):
    create_response = client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    response = client.put(
        f"/api/income/{income_id}",
        json={
            "description": "Updated Salary",
            "amount": 55000,
            "category": "Salary",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == income_id
    assert data["description"] == "Updated Salary"
    assert data["amount"] == 55000
    assert data["category"] == "Salary"


def test_update_income_not_found(client, test_db):
    response = client.put(
        "/api/income/99999",
        json={
            "description": "Updated Salary",
            "amount": 55000,
            "category": "Salary",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Income not found"


def test_delete_income(client, test_db):
    create_response = client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    response = client.delete(
        f"/api/income/{income_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Income deleted successfully"
    )

    get_response = client.get(
        f"/api/income/{income_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Income not found"


def test_delete_income_not_found(client, test_db):
    response = client.delete(
        "/api/income/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Income not found"


def test_get_total_income(client, test_db):
    client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    client.post(
        "/api/income",
        json={
            "description": "Freelance Work",
            "amount": 10000,
            "category": "Freelance",
        },
    )

    client.post(
        "/api/income",
        json={
            "description": "Bonus",
            "amount": 5000,
            "category": "Salary",
        },
    )

    response = client.get(
        "/api/income/total/summary"
    )

    assert response.status_code == 200
    assert response.json()["total"] == 65000


def test_get_income_by_category(client, test_db):
    client.post(
        "/api/income",
        json={
            "description": "Monthly Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    client.post(
        "/api/income",
        json={
            "description": "Freelance Work",
            "amount": 10000,
            "category": "Freelance",
        },
    )

    client.post(
        "/api/income",
        json={
            "description": "Bonus",
            "amount": 5000,
            "category": "Salary",
        },
    )

    response = client.get(
        "/api/income/category/Salary"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert all(
        income["category"] == "Salary"
        for income in data
    )

    amounts = [
        income["amount"]
        for income in data
    ]

    assert 50000 in amounts
    assert 5000 in amounts


def test_income_is_user_scoped(client, test_db):
    client.post(
        "/api/income",
        json={
            "description": "Private Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    response = client.get(
        "/api/income"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["description"] == "Private Salary"


def test_user_cannot_access_other_users_income(
    client,
    test_db,
    monkeypatch,
):
    create_response = client.post(
        "/api/income",
        json={
            "description": "User One Salary",
            "amount": 50000,
            "category": "Salary",
        },
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    from app.api.auth import get_current_user

    async def other_user():
        return {
            "id": "00000000-0000-0000-0000-000000000002",
            "email": "other@example.com",
        }

    from app.api.main import app

    app.dependency_overrides[
        get_current_user
    ] = other_user

    try:
        response = client.get(
            f"/api/income/{income_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Income not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )
