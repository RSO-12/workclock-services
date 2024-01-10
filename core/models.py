from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gmail = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean)
    created_by = db.Column(db.Integer)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.String)
    previous_event_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    event_type_id = db.Column(db.Integer)


class EventType(db.Model):
    __tablename__ = 'event_types'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    is_paid = db.Column(db.Boolean)