"""
home.dash.models
================

The models for the web interface, this defines a User to enable authentication.
"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from home import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(250))
    registered_on = db.Column(db.DateTime, nullable=False, index=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
