from database.models import User
from users import users_service


class RegisterException(Exception):
    pass


class WrongDataException(RegisterException):
    pass


class UserExistsException(RegisterException):
    pass


def register(session, login, password):
    if not users_service.validate_login(login):
        raise WrongDataException("Wrong login")

    if not users_service.validate_password(password):
        raise WrongDataException("Wrong password")

    if users_service.has_user(session, login):
        raise UserExistsException("User exists")

    with session:
        users_service.create_user(session, login, password)


def login(session, login, password) -> User:
    return users_service.login(session, login, password)
