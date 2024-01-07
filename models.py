from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.String(56), primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(97), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# TODO: Make a Token Blacklist center

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