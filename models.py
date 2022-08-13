from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# https://www.youtube.com/watch?v=v6b4tggM7M0


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(250), nullable=True)
    shows = db.relationship("Show", backref="venue", lazy=True)
    genres = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime(), nullable=True)


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_description = db.Column(db.String(250), nullable=True)
    seeking_venue = db.Column(db.Boolean(), default=False)
    shows = db.relationship("Show", backref="artist", lazy=True)
    created_at = db.Column(db.DateTime(), nullable=True)


class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
