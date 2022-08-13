from models import Artist, Venue, Show, db
from sqlalchemy import asc
from flask import render_template, request, flash, url_for, Blueprint
from datetime import datetime
from forms import ShowForm
import sys
import json

show_blueprint = Blueprint("shows", __name__)

#  Shows
#  ----------------------------------------------------------------
class ShowController:
    @show_blueprint.route("/")
    def shows():
        # displays list of shows at /shows
        # TODO: replace with real venues data.
        res_data = Show.query.all()
        data = []
        for res in res_data:
            data.append(
                {
                    "venue_id": res.venue_id,
                    "venue_name": res.venue.name,
                    "artist_id": res.artist_id,
                    "artist_name": res.artist.name,
                    "artist_image_link": res.artist.image_link,
                    "start_time": res.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        return render_template("pages/shows.html", shows=data)

    @show_blueprint.route("/create")
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template("forms/new_show.html", form=form)

    # @tshirts_bluepirnt.route("/edit",methods=["GET"])
    @show_blueprint.route("/create", methods=["POST"])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # TODO: insert form data as a new Show record in the db, instead
        error = False
        try:
            artist_id = request.form["artist_id"]
            venue_id = request.form["venue_id"]
            start_time = request.form["start_time"]
            show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
            db.session.add(show)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

            # on successful db insert, flash success
        if not error:
            flash("Show was successfully listed!")
            # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        if error:
            flash("An error occurred. Show could not be listed.")
        return render_template("pages/home.html")
