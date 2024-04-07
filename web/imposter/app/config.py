from os import environ
import uuid


class Config:
    FLAG = environ.get('FLAG')
    PORT = environ.get('PORT')
    ADMIN_PASSWORD = uuid.uuid4().hex
    SECRET_KEY = uuid.uuid4().hex

    FLASKAPP = "app.py"
    FLASK_DEBUG = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
