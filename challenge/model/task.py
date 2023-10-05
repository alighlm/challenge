from datetime import datetime, timezone
from operator import and_

from challenge.extensions import db
from challenge.model import JobModel, TaskStatus
from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from sqlalchemy.sql.expression import func, text
from sqlalchemy.orm import aliased

from sqlalchemy import Interval


class TaskModel(ResourceMixin, db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    parameters = db.Column(db.Text, default="{}")
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())
    fetch_start_time = db.Column(AwareDateTime(), comment="last fetch start time")
    fetch_end_time = db.Column(AwareDateTime(), comment="last fetch end time")
    fetch_result = db.Column(
        db.Enum(TaskStatus), default=TaskStatus.Idle, comment="last fetch result"
    )
    max_attempt = db.Column(
        db.Integer, default=10, comment="maximum attempt on failure"
    )
    task_interval = db.Column(
        db.Integer, comment="interval time of execution in seconds"
    )
    max_execution_time = db.Column(
        db.Integer, comment="maximum time of execution in seconds"
    )
    attempt = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(TaskModel, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_current_valid_less_than_interval(cls):
        return cls.query.filter(
            (cls.start_time <= datetime.now(timezone.utc))
            & (cls.end_time >= datetime.now(timezone.utc))
            & (
                cls.fetch_end_time
                <= func.DATE_SUB(func.now(), text("interval task_interval SECOND"))
            )
            & (cls.fetch_result == TaskStatus.Finished)
        )

    @classmethod
    def find_all_current_valid_new(cls):
        return cls.query.filter(
            (cls.start_time <= datetime.now(timezone.utc))
            & (cls.end_time >= datetime.now(timezone.utc))
            & (cls.fetch_end_time == None)
            & (cls.fetch_start_time == None)
        )

    @classmethod
    def find_all_lasttime_failed(cls):
        return cls.query.filter(
            (cls.start_time <= datetime.now(timezone.utc))
            & (cls.end_time >= datetime.now(timezone.utc))
            & (cls.fetch_result == TaskStatus.Failed)
            & (cls.attempt < cls.max_attempt)
        )

    @classmethod
    def find_all_tasks(cls):
        query1 = cls.find_all_current_valid_less_than_interval()
        query2 = cls.find_all_current_valid_new()
        query3 = cls.find_all_lasttime_failed()
        return query1.union(query2, query3).all()

    @classmethod
    def reset_attempt(self, task_id: int):
        task = TaskModel.query.get_or_404(task_id)
        if task:
            task.attempt = 0
            task.save()
            return True
