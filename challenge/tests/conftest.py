import pytest

from flask_webtest import TestApp
from challenge.app import create_app
from challenge.extensions import db as _db
from challenge.model import UserModel
from config import settings
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="function")
def app():
    db_uri = "{0}_test".format(settings.SQLALCHEMY_DATABASE_URI)

    params = {
        "DEBUG": False,
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "JWT_HEADER_TYPE": "Bearer",
        "JWT_BLACKLIST_ENABLED": False,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()

    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    yield app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()
