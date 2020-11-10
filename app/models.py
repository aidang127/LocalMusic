from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Artist(db.Model):
    name = db.Column(db.String(64), index=True, unique=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hometown = db.Column(db.String(64), index=True)
    a2es = db.relationship("ArtistToEvent", backref="artist", lazy="dynamic")

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64), index=True)
    state =db.Column(db.String(2), index=True)
    events = db.relationship("Event", backref="venue", lazy="dynamic")

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.DateTime, index=True)
    venueID = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    a2es = db.relationship("ArtistToEvent", backref="event", lazy="dynamic")

class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
