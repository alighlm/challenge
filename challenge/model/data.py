from challenge.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class DataModel(ResourceMixin, db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    data_id = db.Column(db.String(255))
    name_first = db.Column(db.String(255))
    name_last = db.Column(db.String(255))
    decription = db.Column(db.String(255))
    title = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super(DataModel, self).__init__(**kwargs)

    @classmethod
    def find_by_job_id(cls, job_id: int):
        return cls.query.filter_by(job_id=job_id).all()
