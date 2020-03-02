# ---------------------------------------------------------------------------#
# Imports
# ---------------------------------------------------------------------------#
import dateutil.parser
import babel
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate

# ---------------------------------------------------------------------------#
# App Config.
# ---------------------------------------------------------------------------#

# TODO: connect to a local postgresql database: done in config.py

app = Flask(__name__)
moment = Moment(app)
#app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# ---------------------------------------------------------------------------#
# Attach Migrate Class
# ---------------------------------------------------------------------------#
migrate = Migrate(app, db)


# ---------------------------------------------------------------------------#
# Filters.
# ---------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# -----------------------------------------------------------------------------#
# Blueprints.
# -----------------------------------------------------------------------------#

from fyyur.core.controllers import core
from fyyur.artists.controllers import artist
from fyyur.venues.controllers import venue
from fyyur.shows.controllers import show
from fyyur.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(core)
app.register_blueprint(artist)
app.register_blueprint(venue)
app.register_blueprint(show)
app.register_blueprint(error_pages)
