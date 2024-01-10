from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.String(56), primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(97), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Notebook(db.Model):
    id = db.Column(
        db.String(56),
        primary_key=True
    )
    author = db.Column(
        db.String(56),
        db.ForeignKey('user.id')
    )
    name = db.Column(
        db.String(500)
    )
    description = db.Column(
        db.Text()
    )
    timestamp = db.Column(
        db.Float()
    )

class Page(db.Model):
    id = db.Column(
        db.String(56),
        primary_key=True
    )
    author = db.Column(
        db.String('56'),
        db.ForeignKey('user.id')
    )
    notebook = db.Column(
        db.String(56),
        db.ForeignKey('notebook.id')
    )
    content = db.Column(
        db.BLOB()
    )

class RefreshTokenTable(db.Model):
    id = db.Column(
        db.String(56),
        primary_key=True
    )
    token = db.Column(
        db.String(400)
    )
    timestamp = db.Column(
        db.Float()
    )