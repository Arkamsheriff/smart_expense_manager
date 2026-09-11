def test_get_goals_empty(client, test_db):
    response = client.get("/api/goals")

    assert response.status_code == 200
    assert response.json() == []


def test_create_goal(client, test_db):
    response = client.post(
        "/api/goals",
        json={
            "name": "New Car",
            "target_amount": 500000,
            "current_amount": 50000,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "New Car"
    assert data["target_amount"] == 500000
    assert data["current_amount"] == 50000
    assert data["remaining"] == 450000
    assert data["percentComplete"] == 10


def test_get_goal(client, test_db):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Emergency Fund",
            "target_amount": 100000,
            "current_amount": 25000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

    response = client.get(
        f"/api/goals/{goal_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == goal_id
    assert data["name"] == "Emergency Fund"
    assert data["remaining"] == 75000
    assert data["percentComplete"] == 25


def test_get_goal_not_found(client, test_db):
    response = client.get(
        "/api/goals/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"


def test_create_goal_invalid_target(client, test_db):
    response = client.post(
        "/api/goals",
        json={
            "name": "Invalid Goal",
            "target_amount": 0,
            "current_amount": 0,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Target amount must be greater than 0"
    )


def test_create_goal_negative_current_amount(
    client,
    test_db,
):
    response = client.post(
        "/api/goals",
        json={
            "name": "Invalid Goal",
            "target_amount": 100000,
            "current_amount": -1,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Current amount cannot be negative"
    )


def test_create_goal_empty_name(client, test_db):
    response = client.post(
        "/api/goals",
        json={
            "name": "   ",
            "target_amount": 100000,
            "current_amount": 0,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Goal name cannot be empty"
    )


def test_update_goal(client, test_db):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Old Goal",
            "target_amount": 100000,
            "current_amount": 10000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

    response = client.put(
        f"/api/goals/{goal_id}",
        json={
            "name": "Updated Goal",
            "target_amount": 200000,
            "current_amount": 50000,
            "target_date": "2028-12-31",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Goal"
    assert data["target_amount"] == 200000
    assert data["current_amount"] == 50000
    assert data["remaining"] == 150000
    assert data["percentComplete"] == 25


def test_update_goal_not_found(client, test_db):
    response = client.put(
        "/api/goals/99999",
        json={
            "name": "Missing Goal",
            "target_amount": 100000,
            "current_amount": 0,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"


def test_delete_goal(client, test_db):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Delete Me",
            "target_amount": 50000,
            "current_amount": 5000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

    response = client.delete(
        f"/api/goals/{goal_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/goals/{goal_id}"
    )

    assert get_response.status_code == 404


def test_delete_goal_not_found(client, test_db):
    response = client.delete(
        "/api/goals/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"


def test_goals_are_user_scoped(client, test_db):
    response = client.post(
        "/api/goals",
        json={
            "name": "Private Goal",
            "target_amount": 100000,
            "current_amount": 10000,
            "target_date": "2027-12-31",
        },
    )

    assert response.status_code == 201

    response = client.get(
        "/api/goals"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Private Goal"


def test_user_cannot_access_other_users_goal(
    client,
    test_db,
):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Private Goal",
            "target_amount": 100000,
            "current_amount": 10000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

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
            f"/api/goals/{goal_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )


def test_user_cannot_update_other_users_goal(
    client,
    test_db,
):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Private Goal",
            "target_amount": 100000,
            "current_amount": 10000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

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
            f"/api/goals/{goal_id}",
            json={
                "name": "Hacked Goal",
                "target_amount": 999999,
                "current_amount": 999999,
                "target_date": "2030-01-01",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )


def test_user_cannot_delete_other_users_goal(
    client,
    test_db,
):
    create_response = client.post(
        "/api/goals",
        json={
            "name": "Private Goal",
            "target_amount": 100000,
            "current_amount": 10000,
            "target_date": "2027-12-31",
        },
    )

    assert create_response.status_code == 201

    goal_id = create_response.json()["id"]

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
            f"/api/goals/{goal_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None,
        )
