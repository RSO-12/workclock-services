from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)