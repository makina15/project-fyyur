from fyyur import db
from fyyur.models import City, Venue, Artist, Show, State, Genre
from flask import flash, redirect, url_for
from flask import render_template, request, Blueprint
from sqlalchemy.sql.expression import and_
import datetime as dt
from fyyur.artists.forms import ArtistForm
from sqlalchemy.exc import SQLAlchemyError


#  Artists
#  ----------------------------------------------------------------
artist = Blueprint('artist', __name__)

@artist.route('/artists')
def artists():
    artist = Artist.query.all()
    data = []
    if len(artist) > 0:
        for item in artist:
            data.append({"id": item.id, "name": item.name})
    return render_template('pages/artists.html', artists=data)


@artist.route('/artists/search', methods=['POST'])
def search_artists():
    search_str = request.form.get('search_term', '')
    response = dict()
    artist_list = Artist.query.filter(Artist.name.ilike(r"%{}%".format(search_str))).all()
    response["count"] = len(artist_list)
    response["data"] = []
    if response["count"] > 0:
        for item in artist_list:
            show_count = (
                Show.query.filter(
                    and_(Show.start_time >= dt.datetime.now(), Show.artist_id == item.id)
                ).count()
            )
            response["data"].append({"id": item.id, "name": item.name, "num_upcoming_shows": show_count})
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@artist.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = {}
    artist = Artist.query.get(artist_id)
    if artist:
        city_obj = City.query.get(artist.city_id)
        past_show_list = Show.query.filter(and_(Show.start_time <= dt.datetime.now(), Show.artist_id == artist.id)).all()
        next_show_list = Show.query.filter(and_(Show.start_time >= dt.datetime.now(), Show.artist_id == artist.id)).all()
        past_shows = []
        next_shows = []

        if len(past_show_list) > 0:
            for item in past_show_list:
                venue = item.venue_
                past_shows.append(
                    {"venue_id": venue.id,
                     "venue_name": venue.name,
                     "venue_image_link": venue.image_link,
                     "start_time": item.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                     }
                )
        if len(next_show_list) > 0:
            for item in next_show_list:
                venue = item.venue_
                next_shows.append(
                    {"venue_id": venue.id,
                     "venue_name": venue.name,
                     "venue_image_link": venue.image_link,
                     "start_time": item.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                     }
                )
        data.update({
            "id": artist.id,
            "name": artist.name,
            "genres": [item.genre for item in artist.genres],
            "city": city_obj.city,
            "state": city_obj.state_.state,
            "phone": artist.phone,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": next_shows,
            "past_shows_count": len(past_show_list),
            "upcoming_shows_count": len(next_show_list)
        })
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@artist.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_obj = Artist.query.get(artist_id)
    city_obj = City.query.get(artist_obj.city_id)

    artist = dict()
    if artist_obj:
        artist.update({
            "id": artist_obj.id,
            "name": artist_obj.name,
            "genres": [item.genre for item in artist_obj.genres],
            "city": city_obj.city,
            "state": city_obj.state_.state,
            "phone": artist_obj.phone,
            "facebook_link": artist_obj.facebook_link,
            "seeking_venue": artist_obj.seeking_venue,
            "seeking_description": artist_obj.seeking_description,
            "image_link": artist_obj.image_link
        })
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artist.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    city = request.form["city"]
    state = request.form["state"]
    artist_obj = Artist.query.get(artist_id)

    # Need to detect if the city and state is already in the database or not
    city_obj = City.query.filter_by(city=city).first()
    state_obj = State.query.filter_by(state=state).first()

    if city_obj:
        artist_obj.city_id = city_obj.id
    elif state_obj:
        city_obj = City(city=city)
        city_obj.state_id = state_obj.id
    else:
        state_obj = State(state=state)
        city_obj = City(city=city)
        artist_obj.city_ = city_obj
        city_obj.state_ = state_obj
    try:
        artist_obj.name = request.form["name"]
        artist_obj.phone = request.form["phone"]
        artist_obj.website = request.form.get("website")
        artist_obj.image_link = request.form.get("image_link")
        artist_obj.facebook_link = request.form["facebook_link"]
        artist_obj.genres = []
        for idx in request.form.getlist("genres"):
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                artist_obj.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                artist_obj.genres.append(genre)
        db.session.commit()
        flash("Artist info. edited.")
        return redirect(url_for('artist.show_artist', artist_id=artist_id))
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash("Sorry, Can not Edit.")
        return redirect(url_for('artist.show_artist', artist_id=artist_id))
    finally:
        db.session.close()



#  Create Artist
#  ----------------------------------------------------------------
@artist.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@artist.route('/artists/create', methods=['POST'])
def create_artist_submission():
    name = request.form["name"]
    city = request.form["city"]
    state = request.form["state"]
    phone = request.form["phone"]
    website = request.form.get("website")
    image_link = request.form.get("image_link")
    facebook_link = request.form["facebook_link"]
    genres = request.form.getlist("genres")
    try:
        artist = Artist(name=name, phone=phone, website=website, facebook_link=facebook_link, image_link=image_link)
        state_obj = State.query.filter_by(state=state).first()
        city_obj = City.query.filter_by(city=city).first()

        if state_obj:
            if city_obj:
                artist.city_id = city_obj.id
            else:
                city_obj = City(city=city)
                city_obj.state_id = state_obj.id
                artist.city_ = city_obj
        else:
            state_obj = State(state=state)
            city_obj = City(city=city)
            artist.city_ = city_obj
            city_obj.state_ = state_obj

        for idx in genres:
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                artist.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                artist.genres.append(genre)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + name + ' was successfully listed!')
        return render_template('pages/home.html')
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash('Show was not listed!')
        return render_template('errors/404.html')
    finally:
        db.session.close()
