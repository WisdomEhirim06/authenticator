from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.String(10), nullable=False)
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    email =db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11))

    def __repr__(self):
        return f"<User {self.email}>"