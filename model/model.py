from db.db import db
from datetime import datetime   


class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    user_sno = db.Column(db.Integer,db.ForeignKey('user.sno'), nullable=False)

class User(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    todo = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

