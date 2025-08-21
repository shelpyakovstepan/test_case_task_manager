# STDLIB
from datetime import UTC, datetime, timedelta

# THIRDPARTY
import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.config import settings
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Отдаёт хешированный пароль.

    Args:
        password: Пароль, который должен быть захеширован.

    Returns:
        Захешированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнивает введённый пароль и хешированный пароль.

    Args:
        plain_password: Введенный пароль.
        hashed_password: Хешированный пароль для сравнения.

    Returns:
        True, если пароль правильный, False - если неправильный.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создаёт JWT токен.

    Args:
        data: Данные для создания JWT токена.

    Returns:
        encoded_jwt: Созданный JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(session: AsyncSession, email: EmailStr, password: str):
    """
    Аутентифицирует пользователя.

    Args:
        email: Email рользователя, который должен быть аутентифицирован.
        password: Пароль, по которому проверяется пользователь.

    Returns:
        auth_user: Экземпляр модели Users, представляющий аутентифицированного пользователя.
        None, если аутентификация не была успешной.
    """
    auth_user = await UsersDAO.find_one_or_none(session=session, email=email)
    if not auth_user:
        return None
    if not verify_password(password, auth_user.hashed_password):
        return None
    return auth_user
