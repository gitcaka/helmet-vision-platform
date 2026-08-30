import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def configure_sqlite_connection(dbapi_connection, _connection_record):
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=10000")
    cursor.close()


class BaseModel(db.Model):
    __abstract__ = True
    __sensitive_fields__ = set()

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in self.__sensitive_fields__
        }


class User(BaseModel):
    __tablename__ = "users"
    __sensitive_fields__ = {"password_hash"}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Log(BaseModel):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    type = db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(80), nullable=False, index=True)
    camera = db.Column(db.String(80), default="", nullable=False)
    score = db.Column(db.String(80), default="", nullable=False)
    title = db.Column(db.String(80), default="", nullable=False)
    location = db.Column(db.String(80), default="", nullable=False)
    img = db.Column(db.String(512), default="", nullable=False)


class Traffic(BaseModel):
    __tablename__ = "traffic"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), unique=True, nullable=False, index=True)
    total = db.Column(db.Integer, default=0, nullable=False)
    ele = db.Column(db.Integer, default=0, nullable=False)
    helmet = db.Column(db.Integer, default=0, nullable=False)
    noHelmet = db.Column(db.Integer, default=0, nullable=False)
