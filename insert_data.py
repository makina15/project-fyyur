from fyyur.models import State, City, Venue, Artist, Genre, Show
from fyyur import db
import datetime
import random

"""
Relation:
    Parent          Child
    State           City
    City            Artist, Venue
    Venue, Artist   Shows
    Artist          Gener

State and Gener class if independent of foreign key.
"""

# # Insert Data City, State
# state_data = State(state="NY")
# city_data = City(city="New York")
# city_data.state_ = state_data
# db.session.add(state_data)
# db.session.commit()

# Insert Data Venue
venue_list = [
    {
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    },
    {
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
    },
    {
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
    }
]


def insert_venue_data(venues):
    for item in venues:
        venue = Venue(
            id = item.get("id"),
            name=item.get("name"),
            address=item.get("address"),
            phone=item.get("phone"),
            website=item.get("website"),
            image_link=item.get("image_link"),
            facebook_link=item.get("facebook_link"),
            seeking_talent=item.get("seeking_talent"),
            seeking_description=item.get("seeking_description")
            )

        state = State.query.filter_by(state=item.get("state")).first()
        city = City.query.filter_by(city=item.get("city")).first()
        if state:
            if city:
                venue.city_id = city.id
            else:
                city = City(city=item.get("city"))
                city.state_id = state.id
        else:
            state = State(state=item.get("state"))
            city = City(city=item.get("city"))
            city.state_ = state
            venue.city_ = city


        # venue.geners = gener_list
        db.session.add(venue)
        db.session.commit()
        print("Inserted {}".format(item.get("name")))
    return print("All Venue Inserted")


def insert_venue_genres(venues):
    for item in venues:
        venue = Venue.query.filter_by(name=item.get("name")).first()
        for idx in item.get("genres"):
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                venue.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                venue.genres = [genre]
            db.session.commit()


artist_list = [
    {
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    },
    {
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    },
    {
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    }
]


def insert_artist_data(artists):
        for item in artists:
            artist = Artist(
                id=item.get("id"),
                name=item.get("name"),
                phone=item.get("phone"),
                website=item.get("website"),
                facebook_link=item.get("facebook_link"),
                image_link=item.get("image_link"),
                seeking_venue=item.get("seeking_venue"),
                seeking_description=item.get("seeking_description")
                )

            state = State.query.filter_by(state=item.get("state")).first()
            city = City.query.filter_by(city=item.get("city")).first()
            if state:
                if city:
                    artist.city_id = city.id
                else:
                    city = City(city=item.get("city"))
                    city.state_id = state.id
            else:
                state = State(state=item.get("state"))
                city = City(city=item.get("city"))
                artist.city_ = city
                city.state_ = state

            # venue.geners = gener_list
            db.session.add(artist)
            db.session.commit()
            print("Inserted {}".format(item.get("name")))
        print("Artist insertion finished.")
        return print("All Artist Inserted")


def insert_artist_genre(artists):
    for item in artists:
        artist = Artist.query.filter_by(name=item.get("name")).first()
        for idx in item.get("genres"):
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                artist.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                artist.genres = [genre]
            db.session.add(artist)
            db.session.commit()


show_list = [
    {
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
    },
    {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
    },
    {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
    },
    {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
    },
    {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
}
]


def convert_datetime(date_str):
    start_date = datetime.datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S.%f%z')
    end_date = start_date + datetime.timedelta(minutes=random.choice([60, 90, 120]))
    return start_date, end_date


def insert_show_data(shows):
    for item in show_list:
        start_time, end_time = convert_datetime(item.get("start_time"))
        show = Show(
            start_time=start_time,
            end_time=end_time,
            venue_id=item.get("venue_id"),
            artist_id=item.get("artist_id")
        )
        db.session.add(show)
        db.session.commit()
    return print("All show Inserted")


if __name__ == "__main__":
    insert_venue_data(venue_list)
    insert_venue_genres(venue_list)
    insert_artist_data(artist_list)
    insert_artist_genre(artist_list)
    insert_show_data(show_list)
