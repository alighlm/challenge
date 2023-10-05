from datetime import datetime, timezone
from operator import and_

from challenge.extensions import db
from challenge.model import JobModel, TaskStatus
from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from sqlalchemy.sql.expression import func, text
from sqlalchemy.orm import aliased

from sqlalchemy import Interval


class UserModel(ResourceMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
