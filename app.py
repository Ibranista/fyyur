# don't forget to change the past_shows after print checking inside the Artist-Controller.
# https://medium.com/thedevproject/flask-blueprints-complete-tutorial-to-fully-understand-how-to-use-it-767f7433a02e
# from flask import Blueprint
# product = Blueprint('product', __name__)
# @product.route("/listOfClothes")
# def list_of_clothes():
# return "List of clothes"
# @product.route("/listOfShoes")
# def list_of_shoes():
# return "List of shoes"
# @product.route("/listOfTshirts")
# def list_of_tshirts():
# return "List of t-shirts"
# from blueprints.about.views import about
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from sqlalchemy import asc
import json
import sys
import dateutil.parser
import babel
from flask import render_template, Flask, redirect, request, url_for
from models import db, Venue, Artist, Show
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from datetime import datetime
from blueprints.Index_Routes import index_blueprint
from blueprints.Venue_Routes import venue_blueprint
from blueprints.Artist_Routes import artist_blueprint
from blueprints.Show_Routes import show_blueprint
from forms import VenueForm

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

app.register_blueprint(index_blueprint)
# how did he parse t-shirts from register_blueprint
# search for the register_blueprint method or just use express.js style


@app.route("/")
def index():
    most_recent_artists = Artist.query.order_by(
        asc(Artist.created_at)).limit(10).all()
    most_recent_venues = Venue.query.order_by(
        asc(Venue.created_at)).limit(10).all()
    return render_template(
        "pages/home.html",
        most_recent_artists=most_recent_artists,
        most_recent_venues=most_recent_venues,
    )


app.register_blueprint(venue_blueprint, url_prefix="/venues")
app.register_blueprint(artist_blueprint, url_prefix="/artists")
app.register_blueprint(show_blueprint, url_prefix="/shows")

# ----------------------------------------------------------------------------#
# Error Handlers.
# ----------------------------------------------------------------------------#


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


# ----------------------------------------------------------------------------#
# App Debugger.
# ----------------------------------------------------------------------------#
if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# App Launcher.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
