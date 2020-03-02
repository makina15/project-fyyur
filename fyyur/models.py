from fyyur import db


# ---------------------------------------------------------------------------#
# Models.
# ---------------------------------------------------------------------------#
class State(db.Model):
    __tablename__ = 'State'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(120), nullable=False, unique=True)
    cities = db.relationship('City', backref='state_', lazy=True)


class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False, unique=True)
    state_id = db.Column(db.Integer, db.ForeignKey('State.id'), nullable=False)
    venues = db.relationship('Venue', backref='city_', lazy=True)
    artists = db.relationship('Artist', backref='city_', lazy=True)


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(120), nullable=False, unique=True)


# Many to Many association table for venue and genres
venue_genres = db.Table(
    'Venue_Genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(256))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, unique=False, default=True)
    seeking_description = db.Column(db.Text(), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    shows = db.relationship('Show', backref='venue_', lazy=True)
    genres = db.relationship(
        'Genre', secondary=venue_genres, lazy='subquery', backref=db.backref('venue_', lazy='dynamic')
    )


# Many to many association table for artist and genres
artist_genres = db.Table(
  'Artist_Genres',
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(256))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    shows = db.relationship('Show', backref='_artist', lazy=True)
    seeking_venue = db.Column(db.Boolean, unique=False, default=True)
    seeking_description = db.Column(db.Text(), nullable=True)
    shows = db.relationship('Show', backref='artist_', lazy=True)
    genres = db.relationship(
        'Genre', secondary=artist_genres, lazy='subquery', backref=db.backref('_artist', lazy=True)
    )

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
