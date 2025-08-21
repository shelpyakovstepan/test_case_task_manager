# THIRDPARTY
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.users.dao import UsersDAO
from app.users.models import Users


class TestUsersDAO:
    @pytest.mark.parametrize(
        "email, hashed_password",
        [
            (
                "sometest@email.com",
                "$2b$12$pzW2JBdkHmP8yYdq.m4t0OICxBbSjyTA08dLbSzawG.FWqQiYTdqu",
            )
        ],
    )
    async def test_add(
        self, get_session: AsyncSession, email: str, hashed_password: str
    ):
        user = await UsersDAO.add(
            session=get_session, email=email, hashed_password=hashed_password
        )

        assert user is not None
        assert user.email == email
        assert user.hashed_password == hashed_password

    async def test_find_by_id(self, get_session: AsyncSession, create_user: Users):
        user = await UsersDAO.find_by_id(session=get_session, model_id=create_user.uuid)

        assert user is not None
        assert user.email == create_user.email

    async def test_find_by_id_fail(self, get_session: AsyncSession):
        user = await UsersDAO.find_by_id(
            session=get_session, model_id="dcf11111-1111-1111-b1b1-c111c1fbe111"
        )

        assert user is None

    @pytest.mark.parametrize(
        "email, exists",
        [
            ("somenotexists@email.com", False),
            ("test@test.com", True),
        ],
    )
    async def test_find_one_or_none(
        self, get_session: AsyncSession, create_user: Users, email: str, exists: bool
    ):
        user = await UsersDAO.find_one_or_none(session=get_session, email=email)

        if exists:
            assert user is not None
            assert user.email == email
        else:
            assert user is None
