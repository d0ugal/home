"""
home.webcam.models
==================

The models for storing the webcam details
"""

from home import db


class Webcam(db.Model):
    __tablename__ = "webcams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    filename = db.Column(db.String(20), unique=True, index=True)
    url = db.Column(db.String(250))
    created_on = db.Column(db.DateTime, nullable=False, index=True)

    @property
    def full_path(self):
        return '/static/media/%s' % self.filename

    def __repr__(self):
        return '<Webcam %r>' % (self.name)
