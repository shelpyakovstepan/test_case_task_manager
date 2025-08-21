# THIRDPARTY
from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectUserEmailOrPasswordException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class TokenExpiredException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectTokenFormatException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED


class NotUserException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Not user"


class NotTaskException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Not task"


class YouCanNotUpdateTaskException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "You can not update task"
