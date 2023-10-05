from flask import Flask, jsonify
from celery import Celery
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from .extensions import db
from challenge.model import *
from challenge.resource.task import blp as TaskBlueprint
from challenge.resource.user import blp as UserBlueprint
from .model.token_blocklist import TokenBlocklist

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

    api = Api(app)
    api.register_blueprint(TaskBlueprint)
    api.register_blueprint(UserBlueprint)
    db.init_app(app)
    jwt_callback_functions(app)


def jwt_callback_functions(app):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # login_manager.init_app(challenge)
    # limiter.init_app(challenge)

    return None
