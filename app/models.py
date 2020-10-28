from app import db

class Artist(db.Model):
    name = db.Column(db.String(64), index=True, unique=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hometown = db.Column(db.String(64), index=True, unique=True)
    a2es = db.relationship("ArtistToEvent", backref="artist", lazy="dynamic")

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    events = db.relationship("Event", backref="venue", lazy="dynamic")

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    venueID = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    a2es = db.relationship("ArtistToEvent", backref="event", lazy="dynamic")

class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
