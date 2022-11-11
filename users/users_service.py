import re
from typing import List

import bcrypt
from sqlalchemy.orm.session import Session

from database.models import User

LOGIN_RE = r"^[a-zA-Z0-9]+$"


def validate_login(login: str):
    if not len(login) > 3:
        return False

    return re.match(LOGIN_RE, login) is not None


def validate_password(password):
    return len(password) > 4


def has_user(session: Session, login: str):
    return session.query(User.id).filter_by(login=login).first() is not None


def login(session: Session, login: str, password: str):
    user = session.query(User).filter_by(login=login).first()
    if user is None:
        return None

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return None

    return user


def create_user(session: Session, login: str, password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    user = User(login=login, password=password)
    session.add(user)
    session.commit()


def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()


def get_one(session: Session, id: int) -> User:
    return session.query(User).filter_by(id=id).one()


def remove_user(session: Session, login):
    session.query(User).filter_by(login=login).delete()    
