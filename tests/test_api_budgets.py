def test_get_budgets_empty(client, test_db):
    response = client.get("/api/budgets")

    assert response.status_code == 200
    assert response.json() == []


def test_create_budget(client, test_db):
    response = client.post(
        "/api/budgets",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["category"] == "Food"
    assert data["amount"] == 5000
    assert data["period"] == "monthly"
    assert data["spent"] == 0
    assert data["remaining"] == 5000
    assert data["percentUsed"] == 0


def test_get_budget(client, test_db):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    response = client.get(
        f"/api/budgets/{budget_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == budget_id
    assert data["category"] == "Food"
    assert data["amount"] == 5000
    assert data["period"] == "monthly"


def test_get_budget_not_found(client, test_db):
    response = client.get(
        "/api/budgets/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Budget not found"


def test_update_budget(client, test_db):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    response = client.put(
        f"/api/budgets/{budget_id}",
        json={
            "category": "Travel",
            "amount": 8000,
            "period": "monthly",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == budget_id
    assert data["category"] == "Travel"
    assert data["amount"] == 8000
    assert data["period"] == "monthly"
    assert data["spent"] == 0
    assert data["remaining"] == 8000
    assert data["percentUsed"] == 0


def test_update_budget_not_found(client, test_db):
    response = client.put(
        "/api/budgets/99999",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Budget not found"


def test_delete_budget(client, test_db):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    response = client.delete(
        f"/api/budgets/{budget_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Budget deleted successfully"
    )

    get_response = client.get(
        f"/api/budgets/{budget_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Budget not found"


def test_delete_budget_not_found(client, test_db):
    response = client.delete(
        "/api/budgets/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Budget not found"


def test_budget_is_user_scoped(client, test_db):
    response = client.post(
        "/api/budgets",
        json={
            "category": "Food",
            "amount": 5000,
            "period": "monthly",
        },
    )

    assert response.status_code == 200

    budgets = client.get(
        "/api/budgets"
    )

    assert budgets.status_code == 200

    data = budgets.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_user_cannot_access_other_users_budget(
    client,
    test_db,
):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Private",
            "amount": 10000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    from app.api.auth import get_current_user
    from app.api.main import app

    async def other_user():
        return {
            "id": "00000000-0000-0000-0000-000000000002",
            "email": "other@example.com",
        }

    app.dependency_overrides[
        get_current_user
    ] = other_user

    try:
        response = client.get(
            f"/api/budgets/{budget_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Budget not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )


def test_user_cannot_update_other_users_budget(
    client,
    test_db,
):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Private",
            "amount": 10000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    from app.api.auth import get_current_user
    from app.api.main import app

    async def other_user():
        return {
            "id": "00000000-0000-0000-0000-000000000002",
            "email": "other@example.com",
        }

    app.dependency_overrides[
        get_current_user
    ] = other_user

    try:
        response = client.put(
            f"/api/budgets/{budget_id}",
            json={
                "category": "Hacked",
                "amount": 99999,
                "period": "monthly",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Budget not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )


def test_user_cannot_delete_other_users_budget(
    client,
    test_db,
):
    create_response = client.post(
        "/api/budgets",
        json={
            "category": "Private",
            "amount": 10000,
            "period": "monthly",
        },
    )

    assert create_response.status_code == 200

    budget_id = create_response.json()["id"]

    from app.api.auth import get_current_user
    from app.api.main import app

    async def other_user():
        return {
            "id": "00000000-0000-0000-0000-000000000002",
            "email": "other@example.com",
        }

    app.dependency_overrides[
        get_current_user
    ] = other_user

    try:
        response = client.delete(
            f"/api/budgets/{budget_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Budget not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )
