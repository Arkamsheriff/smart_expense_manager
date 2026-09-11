import asyncio
import httpx
from unittest.mock import patch

from app.api.auth import get_current_user


def run_async(coroutine):
    return asyncio.run(coroutine)


def test_get_current_user_missing_credentials():
    try:
        run_async(get_current_user(None))
        assert False, "Expected HTTPException"
    except Exception as exc:
        assert exc.status_code == 401
        assert exc.detail == "Authentication required"


def test_get_current_user_invalid_scheme():
    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Basic",
            "credentials": "test-token",
        },
    )()

    try:
        run_async(get_current_user(credentials))
        assert False, "Expected HTTPException"
    except Exception as exc:
        assert exc.status_code == 401
        assert exc.detail == "Invalid authentication scheme"


def test_get_current_user_missing_supabase_url(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        None,
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "test-token",
        },
    )()

    try:
        run_async(get_current_user(credentials))
        assert False, "Expected HTTPException"
    except Exception as exc:
        assert exc.status_code == 500
        assert exc.detail == "SUPABASE_URL is not configured"


def test_get_current_user_missing_publishable_key(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        None,
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "test-token",
        },
    )()

    try:
        run_async(get_current_user(credentials))
        assert False, "Expected HTTPException"
    except Exception as exc:
        assert exc.status_code == 500
        assert exc.detail == (
            "SUPABASE_PUBLISHABLE_KEY is not configured"
        )


def test_get_current_user_auth_service_unavailable(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        "test-key",
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "test-token",
        },
    )()

    async def raise_http_error(*args, **kwargs):
        raise httpx.ConnectError("Connection failed")

    with patch(
        "httpx.AsyncClient.get",
        new=raise_http_error,
    ):
        try:
            run_async(get_current_user(credentials))
            assert False, "Expected HTTPException"
        except Exception as exc:
            assert exc.status_code == 503
            assert exc.detail == (
                "Authentication service unavailable"
            )


def test_get_current_user_invalid_token(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        "test-key",
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "invalid-token",
        },
    )()

    mock_response = httpx.Response(
        401,
        json={"error": "invalid token"},
    )

    async def mock_get(*args, **kwargs):
        return mock_response

    with patch(
        "httpx.AsyncClient.get",
        new=mock_get,
    ):
        try:
            run_async(get_current_user(credentials))
            assert False, "Expected HTTPException"
        except Exception as exc:
            assert exc.status_code == 401
            assert exc.detail == (
                "Invalid or expired authentication token"
            )


def test_get_current_user_invalid_auth_response(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        "test-key",
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "test-token",
        },
    )()

    mock_response = httpx.Response(
        200,
        content=b"not-json",
    )

    async def mock_get(*args, **kwargs):
        return mock_response

    with patch(
        "httpx.AsyncClient.get",
        new=mock_get,
    ):
        try:
            run_async(get_current_user(credentials))
            assert False, "Expected HTTPException"
        except Exception as exc:
            assert exc.status_code == 401
            assert exc.detail == (
                "Invalid authentication response"
            )


def test_get_current_user_missing_user_id(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        "test-key",
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "test-token",
        },
    )()

    mock_response = httpx.Response(
        200,
        json={"email": "test@example.com"},
    )

    async def mock_get(*args, **kwargs):
        return mock_response

    with patch(
        "httpx.AsyncClient.get",
        new=mock_get,
    ):
        try:
            run_async(get_current_user(credentials))
            assert False, "Expected HTTPException"
        except Exception as exc:
            assert exc.status_code == 401
            assert exc.detail == (
                "Authenticated user ID not found"
            )


def test_get_current_user_success(monkeypatch):
    monkeypatch.setattr(
        "app.api.auth.SUPABASE_URL",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        "app.api.auth.SUPABASE_PUBLISHABLE_KEY",
        "test-key",
    )

    credentials = type(
        "Credentials",
        (),
        {
            "scheme": "Bearer",
            "credentials": "valid-token",
        },
    )()

    mock_user = {
        "id": "11111111-1111-1111-1111-111111111111",
        "email": "test@example.com",
    }

    mock_response = httpx.Response(
        200,
        json=mock_user,
    )

    async def mock_get(*args, **kwargs):
        return mock_response

    with patch(
        "httpx.AsyncClient.get",
        new=mock_get,
    ):
        user = run_async(
            get_current_user(credentials)
        )

    assert user == mock_user
