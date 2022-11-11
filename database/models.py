from sqlalchemy import Column, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")



class JoinedRoom(Base):
    __tablename__ = "joined_rooms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user = relationship("User")
    room = relationship("Room")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    value = Column(String)
    room = relationship("Room")    

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    value = Column(Float)
    user = relationship("User")
    topic = relationship("Topic")





