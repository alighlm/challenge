import enum
from datetime import datetime
from pydoc import text

from challenge.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class TaskStatus(enum.Enum):
    Idle = 0
    Started = 1
    Finished = 2
    Failed = 3


class JobModel(ResourceMixin, db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("task.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    started_time = db.Column(db.DateTime)
    finished_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.Idle)
    response = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(JobModel, self).__init__(**kwargs)

    @classmethod
    def find_by_task_id(cls, task_id: int):
        return cls.query.filter_by(task_id=task_id).first()

    def job_started(self):
        self.status = TaskStatus.Started
        self.started_time = datetime.now()
        db.session.commit()

    def job_finished(self, status: TaskStatus, response: text):
        self.status = status
        self.finished_time = datetime.now()
        self.response = response
        db.session.commit()

    @classmethod
    def find_last_job_by_task_id(cls, task_id: int):
        return cls.query.filter_by(task_id=task_id).order_by(cls.id.desc()).first()
