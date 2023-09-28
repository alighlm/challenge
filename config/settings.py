import os
from datetime import timedelta


DEBUG = True

SERVER_NAME = "localhost:8000"
SECRET_KEY = "insecurekeyfordev"


# Celery.
CELERY_BROKER_URL = "redis://:devpassword@redis:6379/0"
CELERY_RESULT_BACKEND = "redis://:devpassword@redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_REDIS_MAX_CONNECTIONS = 5


# SQLAlchemy.
db_uri = "mysql+pymysql://root:mysqlpassword@mysql:3306/challenge"
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
