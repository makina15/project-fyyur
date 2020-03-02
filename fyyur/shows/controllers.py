from fyyur import db
from fyyur.models import City, Venue, Artist, Show, State, Genre
from flask import flash, redirect, url_for
from flask import render_template, request, Blueprint
from sqlalchemy.sql.expression import and_
import datetime as dt
from fyyur.shows.forms import ShowForm
from sqlalchemy.exc import SQLAlchemyError



#  Shows
#  ----------------------------------------------------------------
show = Blueprint('show', __name__)

@show.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    show_list = Show.query.all()
    for item in show_list:
        print(item.__dict__.get("start_time").strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    for item in show_list:
        artist_subquery = item.artist_
        venue_subquery = item.venue_
        data.append({
            "venue_id": item.venue_id,
            "venue_name": venue_subquery.name,
            "artist_id": item.artist_id,
            "artist_name": artist_subquery.name,
            "artist_image_link": artist_subquery.image_link,
            "start_time": item.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })
    return render_template('pages/shows.html', shows=data)


@show.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@show.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        artist_id = request.form["artist_id"]
        venue_id = request.form["venue_id"]
        start_time = datetime.strptime(request.form["start_time"], '%Y-%m-%d %H:%M:%S')
        show = Show(
            venue_id=venue_id,
            artist_id=artist_id,
            start_time=start_time,
            end_time=start_time + dt.timedelta(hours=60)
        )
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash('Show was not listed!')
        return render_template('errors/404.html')
    finally:
        db.session.close()
