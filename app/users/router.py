# THIRDPARTY
from fastapi import APIRouter, Depends, Response

# FIRSTPARTY
from app.database import DbSession
from app.exceptions import (
    IncorrectUserEmailOrPasswordException,
    UserAlreadyExistsException,
)
from app.logger import logger
from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUsersAuth

router = APIRouter(prefix="/auth", tags=["Аутентификация & Пользователи"])


@router.post("/register")
async def register(session: DbSession, user_data: SUsersAuth) -> None:
    """
    Создаёт нового пользователя.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        user_data: Pydantic модель SUsersAuth, содержащая данные для создания нового пользователя.

    Returns:
        None
    """
    existing_user = await UsersDAO.find_one_or_none(
        session=session, email=user_data.email
    )
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    await UsersDAO.add(
        session=session, email=user_data.email, hashed_password=hashed_password
    )
    logger.info("User successfully registered")


@router.post("/login")
async def login(response: Response, session: DbSession, user_data: SUsersAuth):
    """
    Аутентифицирует пользователя в системе.

    Args:
        response: Response - Объект ответа FastAPI для установки cookie.
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        user_data: Pydantic модель SUsersAuth, содержащая данные для аутентификации пользователя.

    Returns:
        Созданный access_token.
    """
    user = await authenticate_user(
        session=session, email=user_data.email, password=user_data.password
    )
    if not user:
        raise IncorrectUserEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.uuid)})
    response.set_cookie("access_token", access_token, httponly=True)

    logger.info("User logged in")

    return {"access_token": access_token}


@router.get("/me")
async def get_me(user: Users = Depends(get_current_user)):
    """
    Выдаёт информацию пользователю о самом себе.

    Args:
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        user: Экземпляр модели Users, представляющий пользователя.
    """
    return user


@router.post("/logout")
async def logout_user(response: Response) -> None:
    """Осуществляет выход пользователя из системы"""
    response.delete_cookie("access_token")
    logger.info("User logged out")
