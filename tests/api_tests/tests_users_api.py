# THIRDPARTY
from httpx import AsyncClient
import pytest

# FIRSTPARTY
from app.users.models import Users


class TestUsersApi:
    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("test@test.com", "ffffff", 409),
            ("test@test.com", "f", 422),
            ("abcde", "kotopes", 422),
        ],
    )
    async def test_register(
        self,
        create_user: Users,
        email: str,
        password: str,
        status_code: int,
        ac: AsyncClient,
    ):
        response = await ac.post(
            "/auth/register", json={"email": email, "password": password}
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("test@test.com", "kolobok", 200),
            ("test@test.com", "ffffff", 401),
            ("test@test.com", "f", 422),
            ("abcde", "kotopes", 422),
            ("test@t.com", "kolobok", 401),
        ],
    )
    async def test_login(
        self,
        create_user: Users,
        email: str,
        password: str,
        status_code: int,
        ac: AsyncClient,
    ):
        response = await ac.post(
            "/auth/login", json={"email": email, "password": password}
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "status_code_for_unauthorized_user, status_code_for_authorized_user",
        [(401, 200)],
    )
    async def test_get_me(
        self,
        status_code_for_unauthorized_user: int,
        status_code_for_authorized_user: int,
        ac: AsyncClient,
        authenticated_ac: AsyncClient,
    ):
        unauthorized_user_request_response = await ac.get("/auth/me")
        assert (
            unauthorized_user_request_response.status_code
            == status_code_for_unauthorized_user
        )

        authorized_user_request_response = await authenticated_ac.get("/auth/me")
        assert (
            authorized_user_request_response.status_code
            == status_code_for_authorized_user
        )

    async def test_logout_user(self, authenticated_ac: AsyncClient):
        response = await authenticated_ac.post("/auth/logout")

        assert response.status_code == 200
