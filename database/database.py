import os
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


db_path = os.path.join(os.path.dirname(os.path.abspath(__name__)), "db.sqlite")

db = None
session = None

Base = declarative_base()

DATABASE_NAME = "db2.sqlite"
engine = create_engine(f"sqlite:///{DATABASE_NAME}")
Base = declarative_base()


def get_database() -> sqlite3.Connection:
    global db
    if db is None:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")
    return db


def get_session() -> Session:
    global session
    if session is None:
        session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = session_maker()
    return session


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

