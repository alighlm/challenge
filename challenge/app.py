from flask import Flask
from celery import Celery

from .extensions import db
from challenge.model import *

CELERY_TASK_LIST = [
    "challenge.service.fetch_service",
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        include=CELERY_TASK_LIST,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the challenge factory pattern.

    :param settings_override: Override settings
    :return: Flask challenge
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    if settings_override:
        app.config.update(settings_override)

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the challenge passed in).

    :param app: Flask application instance
    :return: None
    #"""
    # debug_toolbar.init_app(challenge)
    # mail.init_app(challenge)
    # csrf.init_app(challenge)
    db.init_app(app)
    # login_manager.init_app(challenge)
    # limiter.init_app(challenge)

    return None
