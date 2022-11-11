from re import T
from typing import Union

import bcrypt
from sqlalchemy import or_

from database.models import JoinedRoom, Room, User, Topic, Vote

from users.users_service import get_one
from typing import List
from sqlalchemy.orm.session import Session



def create_room(session: Session, owner_id: int, password: str, name: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    room = Room(owner_id=owner_id,password=hashed_password,name=name)
    session.add(room)
    session.flush()
    session.commit()

    if not join_room(session, owner_id, room.id, password):
        raise Exception("Owner could not join the room!")


def get_room(session: Session, id: int):
    db_room = session.query(Room).filter_by(id=id).one()
    if db_room is None:
        return None
    return db_room


def delete_room_by_id(session: Session, id: int):
    session.query(JoinedRoom).filter_by(room_id=id).delete()
    session.query(Room).filter_by(id=id).delete()

def join_room(session: Session, user_id: int, room_id: int, password: str) -> bool:
    room = get_room(session, room_id)
    if room is None:
        return False
    if not bcrypt.checkpw(password.encode("utf-8"), room.password.encode("utf-8")):
        return False

    session.add(JoinedRoom(user_id=user_id,room_id=room_id))

    return True


def joined_room(session: Session, user_id: int, room_id: int) -> bool:
    return (
        session.query(JoinedRoom).filter_by(room_id=room_id, user_id=user_id).count()
        > 0
    )


def room_users(session: Session, room_id: int) -> List[User]:
    return session.query(User).join(JoinedRoom).filter(JoinedRoom.room_id == room_id).all()



def user_rooms(session: Session, user_id: int) -> List[Room]:

    return  session.query(Room).join(JoinedRoom).filter(or_(Room.owner_id == user_id, JoinedRoom.user_id == user_id)).all()


def get_topic(session: Session, room_id: int) -> Union[Topic, None]:
    topic = session.query(Topic).filter_by(room_id=room_id).first()
    if topic is None:
        return None

    return topic


def get_topic_by_id(session: Session, topic_id: int) -> Union[Topic, None]:
    topic = session.query(Topic).filter_by(topic_id=topic_id)
    if topic is None:
        return None

    return topic


def remove_topic(session: Session, room_id: int):
    session.query(Topic).filter_by(room_id=room_id).delete()



def create_topic(session: Session, room_id: int, topic: str):
    session.add(Topic(room_id = room_id, value = topic))


def add_vote(session: Session, topic_id: int, value: float, user_id: int):
    vote = session.query(Vote).filter_by(topic_id=topic_id,user_id=user_id).first()
    if vote is None:
        session.add(Vote(topic_id=topic_id, value=value, user_id=user_id))
        return

    session.query(Vote).filter_by(topic_id=topic_id,user_id=user_id).update({'value': value})


def remove_all_votes(session: Session, topic_id: int):
    session.query(Vote).filter_by(topic_id=topic_id).delete()


def update_password(session: Session, room_id: int, password: str):
    session.query(Room).filter_by(room_id=room_id).update({'password':password})


def get_votes(session: Session, topic_id: int) -> List[Vote]:
    return session.query(Vote).filter_by(topic_id = topic_id).all()
