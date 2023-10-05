from challenge.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class TokenBlocklist(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
