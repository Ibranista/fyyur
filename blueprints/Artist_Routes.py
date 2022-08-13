# don't forget to change the past_shows after print checking this one.
from models import Artist, Venue, db
from sqlalchemy import asc
from flask import render_template, request, flash, redirect, url_for, Blueprint
from datetime import datetime
from forms import ArtistForm
import sys
import json

# product_blueprint = Blueprint('products', __name__)
artist_blueprint = Blueprint("artists", __name__)
# you don't have to write / infront of the url remember when you're using blueprints
#  Artists
#  ----------------------------------------------------------------


class ArtistController:
    @artist_blueprint.route("/")
    def artists():
        # TODO: replace with real data returned from querying the database
        data_res = Artist.query.all()
        data = []
        for item in data_res:
            data.append(
                {
                    "id": item.id,
                    "name": item.name,
                }
            )

        return render_template("pages/artists.html", artists=data)

    @artist_blueprint.route("/search", methods=["POST"])
    def search_artists():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        data_res = request.form.get("search_term")
        data_res = "%{}%".format(data_res)
        data_res = Artist.query.filter(
            Artist.name.ilike(data_res)
            | Artist.city.ilike(data_res)
            | Artist.state.ilike(data_res)
        ).all()
        data = []
        for item in data_res:
            data.append({"id": item.id, "name": item.name,
                        "num_upcoming_shows": 0})
        response = {"count": len(data_res), "data": data}
        return render_template(
            "pages/search_artists.html",
            results=response,
            search_term=request.form.get("search_term", ""),
        )

    @artist_blueprint.route("/<int:artist_id>")
    def show_artist(artist_id):
        # shows the artist page with the given artist_id
        # TODO: replace with real artist data from the artist table, using artist_id
        artist = Artist.query.filter_by(id=artist_id).first()
        past_shows = []
        upcoming_shows = []
        for show in artist.shows:
            show_data = {
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            if datetime.now() > show.start_time:
                past_shows.append(show_data)
            else:
                upcoming_shows.append(show_data)

        data1 = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            #             "past_shows": [{
            #   "venue_id": 1,
            #   "venue_name": "The Musical Hop",
            #   "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            #   "start_time": "2019-05-21T21:30:00.000Z"
            # }],
            "past_shows": past_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows": upcoming_shows,
            "upcoming_shows_count": len(upcoming_shows),
        }
        return render_template("pages/show_artist.html", artist=data1)

    #  Update
    #  ----------------------------------------------------------------
    @artist_blueprint.route("/<int:artist_id>/edit", methods=["GET"])
    def edit_artist(artist_id):
        form = ArtistForm()
        # artist={}
        artist = Artist.query.filter_by(id=artist_id).first()

        form.process()

        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.genres.data = artist.genres
        form.phone.data = artist.phone
        form.website.data = artist.website
        form.facebook_link.data = artist.facebook_link
        form.seeking_venue.default = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.image_link.data = artist.image_link
        # TODO: populate form with fields from artist with ID <artist_id>
        return render_template("forms/edit_artist.html", form=form, artist=artist)

    @artist_blueprint.route("/<int:artist_id>/edit", methods=["POST"])
    def edit_artist_submission(artist_id):
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes
        res_Data = Artist.query.get(artist_id)
        error = False
        try:
            res_Data.name = request.form["name"]
            res_Data.city = request.form["city"]
            res_Data.state = request.form["state"]
            res_Data.genres = request.form.getlist("genres")
            res_Data.phone = request.form["phone"]
            res_Data.image_link = request.form["image_link"]
            res_Data.facebook_link = request.form["facebook_link"]
            res_Data.website = request.form["website"]
            res_Data.seeking_venue = json.loads(
                request.form["seeking_venue"].lower())
            res_Data.seeking_description = request.form["seeking_description"]

            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        # on successful db insert, flash success
        if not error:
            flash("Artist " + request.form["name"] +
                  " was successfully listed!")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        if error:
            flash(
                "An error occurred. Artist " + res_Data.name + " could not be listed."
            )
        return redirect(url_for("artists.show_artist", artist_id=artist_id))

    #  Create Artist
    #  ----------------------------------------------------------------

    @artist_blueprint.route("/create", methods=["GET"])
    def create_artist_form():
        form = ArtistForm()
        return render_template("forms/new_artist.html", form=form)

    @artist_blueprint.route("/create", methods=["POST"])
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # TODO: insert form data as a new Venue record in the db, instead
        # TODO: modify data to be the data object returned from db insertion
        error = False

        try:
            name = request.form["name"]
            city = request.form["city"]
            state = request.form["state"]
            genres = request.form.getlist("genres")
            phone = request.form["phone"]
            image_link = request.form["image_link"]
            facebook_link = request.form["facebook_link"]
            website = request.form["website"]
            seeking_venue = json.loads(request.form["seeking_venue"].lower())
            seeking_description = request.form["seeking_description"]
            created_at = datetime.now()
            stored_Artist = Artist(
                name=name,
                city=city,
                state=state,
                phone=phone,
                genres=genres,
                facebook_link=facebook_link,
                image_link=image_link,
                website=website,
                seeking_venue=seeking_venue,
                seeking_description=seeking_description,
                created_at=created_at,
            )
            db.session.add(stored_Artist)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

            # on successful db insert, flash success
            # flash("Artist " + request.form["name"] + " was successfully listed!")
        if not error:
            flash("Artist " + request.form["name"] +
                  " was successfully listed!")
            # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        if error:
            # on unsuccessful db insert, flash an error.
            # change data name to the name coming from the input
            flash(
                "An error occurred. Artist "
                + request.form["name"]
                + " could not be listed."
            )

        return render_template("pages/home.html")

    @artist_blueprint.route("/<artist_id>", methods=["DELETE"])
    def delete_artist(artist_id):
        error = False
        try:
            artist = Artist.query.get(artist_id)
            # TODO: delete related shows before deleting the artist
            db.session.delete(artist)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            flash(f"An error occurred.")
        if not error:
            flash("Artist was successfully deleted.")

        return redirect(url_for("home.index"))
