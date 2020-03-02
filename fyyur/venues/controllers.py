from fyyur import db
from fyyur.models import City, Venue, Artist, Show, State, Genre
from flask import flash, redirect, url_for
from flask import render_template, request, Blueprint
from sqlalchemy.sql.expression import and_
import datetime as dt
from fyyur.venues.forms import VenueForm
from sqlalchemy.exc import SQLAlchemyError


#  Venues
#  ----------------------------------------------------------------
venue = Blueprint('venue', __name__)

@venue.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    cities = City.query.order_by(City.city.desc()).all()
    for item in cities:
        response = dict()
        venue_list = Venue.query.filter_by(city_id=item.id).all()
        if len(venue_list) > 0:
            venue_info = []
            # using backref to get the state
            response["state"] = item.state_.state
            response["city"] = item.city
            # number of upcoming shows
            for venue in venue_list:
                show_count = (
                  Show.query.filter(
                    and_(Show.start_time >= dt.datetime.now(), Show.venue_id == venue.id)
                  ).count()
                )
                venue_info.append({"id": venue.id, "name": venue.name, "num_upcoming_shows": show_count})
                response["venues"] = venue_info
            data.append(response)
    return render_template('pages/venues.html', areas=data)


@venue.route('/venues/search', methods=['POST'])
def search_venues():
    response = dict()
    search_str = request.form.get('search_term', '')
    venue_list = Venue.query.filter(Venue.name.ilike(r"%{}%".format(search_str))).all()
    response["count"] = len(venue_list)
    response["data"] = []
    if response.get("count") > 0:
        for venue in venue_list:
            show_count = (
                Show.query.filter(
                    and_(Show.start_time >= dt.datetime.now(), Show.venue_id == venue.id)
                ).count()
            )
            response["data"].append({"id": venue.id, "name": venue.name, "num_upcoming_shows": show_count})
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@venue.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = {}
    venue = Venue.query.get(venue_id)
    if venue:
        city_obj = City.query.get(venue.city_id)
        past_show_list = Show.query.filter(and_(Show.start_time <= dt.datetime.now(), Show.venue_id == venue.id)).all()
        next_show_list = Show.query.filter(and_(Show.start_time >= dt.datetime.now(), Show.venue_id == venue.id)).all()
        past_shows = []
        next_shows = []

        if len(past_show_list) > 0:
            for item in past_show_list:
                artist = item.artist_
                past_shows.append(
                    {"artist_id": artist.id,
                     "artist_name": artist.name,
                     "artist_image_link": artist.image_link,
                     "start_time": item.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                     }
                )

        if len(next_show_list) > 0:
            for item in next_show_list:
                artist = item.artist_
                next_shows.append(
                    {"artist_id": artist.id,
                     "artist_name": artist.name,
                     "artist_image_link": artist.image_link,
                     "start_time": item.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                     }
                )

        data.update({
            'id': venue.id,
            'name': venue.name,
            'address': venue.address,
            'phone': venue.phone,
            'website': venue.website,
            'image_link': venue.image_link,
            'facebook_link': venue.facebook_link,
            'seeking_talent': venue.seeking_talent,
            'seeking_description': venue.seeking_description,
            'genres': [item.genre for item in venue.genres],
            'state': city_obj.state_.state,
            'city': city_obj.city,
            'past_shows': past_shows,
            'past_shows_count': len(past_shows),
            'upcoming_shows': next_shows,
            'upcoming_shows_count': len(next_shows)
        }
        )
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------
@venue.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@venue.route('/venues/create', methods=['POST'])
def create_venue_submission():
    name = request.form["name"]
    city = request.form["city"]
    state = request.form["state"]
    phone = request.form["phone"]
    address = request.form["address"]
    website = request.form.get("website")
    image_link = request.form.get("image_link")
    facebook_link = request.form["facebook_link"]
    genres = request.form.getlist("genres")
    try:
        venue = Venue(
            name=name, phone=phone, address=address,
            website=website, facebook_link=facebook_link,
            image_link=image_link
        )
        state_obj = State.query.filter_by(state=state).first()
        city_obj = City.query.filter_by(city=city).first()

        if state_obj:
            if city_obj:
                venue.city_id = city_obj.id
            else:
                city_obj = City(city=city)
                city_obj.state_id = state_obj.id
                venue.city_ = city_obj
        else:
            state_obj = State(state=state)
            city_obj = City(city=city)
            venue.city_ = city_obj
            city_obj.state_ = state_obj

        for idx in genres:
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                venue.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                venue.genres.append(genre)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + name + ' was listed!')
        return render_template('pages/home.html')
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash('Venue ' + request.form['name'] + ' was not listed!')
        return render_template('errors/404.html')
    finally:
        db.session.close()


@venue.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue_obj = Venue.query.get(venue_id)
    try:
        for genres in venue_obj.genres:
            db.session.delete(genres)
        db.session.delete(venue_obj)
        db.session.comit()
    except SQLAlchemyError as e:
        print(e)
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None



@venue.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_obj = Venue.query.get(venue_id)
    city_obj = City.query.get(venue_obj.city_id)
    venue = dict()
    if venue_obj:
        venue.update({
            "id": venue_obj.id,
            "name": venue_obj.name,
            "genres": [item.genre for item in venue_obj.genres],
            "address": venue_obj.address,
            "city": city_obj.city,
            "state": city_obj.state_.state,
            "phone": venue_obj.phone,
            "website": venue_obj.website,
            "facebook_link": venue_obj.facebook_link,
            "seeking_talent": venue_obj.seeking_talent,
            "seeking_description": venue_obj.seeking_description,
            "image_link": venue_obj.image_link
        })
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@venue.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # form = VenueForm(request.form)
    # TODO: take values from the form submitted, and update existing
    city = request.form["city"]
    state = request.form["state"]
    venue_obj = Venue.query.get(venue_id)
    city_obj = City.query.filter_by(city=city).first()
    state_obj = State.query.filter_by(state=state).first()

    # Need to detect if the city and state is already in the database or not
    if city_obj:
        venue_obj.city_id = city_obj.id
    elif state_obj:
        city_obj = City(city=city)
        city_obj.state_id = state_obj.id
    else:
        state_obj = State(state=state)
        city_obj = City(city=city)
        venue_obj.city_ = city_obj
        city_obj.state_ = state_obj
    try:
        venue_obj.name = request.form["name"]
        venue_obj.phone = request.form["phone"]
        venue_obj.website = request.form.get("website")
        venue_obj.image_link = request.form.get("image_link")
        venue_obj.facebook_link = request.form["facebook_link"]
        venue_obj.address = request.form["address"]
        venue_obj.genres = []
        for idx in request.form.getlist("genres"):
            genre = Genre.query.filter_by(genre=idx).first()
            if genre:
                venue_obj.genres.append(genre)
            else:
                genre = Genre(genre=idx)
                venue_obj.genres.append(genre)
        db.session.commit()
        flash("Venue info. edited.")
        return redirect(url_for('venue.show_venue', venue_id=venue_id))
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash("Sorry, Can not Edit.")
        return redirect(url_for('venue.show_venue', venue_id=venue_id))
    finally:
        db.session.close()
