from models import Artist, Venue, db
from sqlalchemy import asc
from flask import render_template, request, flash, redirect, url_for, Blueprint
from datetime import datetime
from forms import VenueForm
import sys
import json

# https://itnext.io/beginning-with-flask-project-the-5-most-important-information-to-know-before-starting-f075e0fb0aec
# product_blueprint = Blueprint('products', __name__)
venue_blueprint = Blueprint("venues", __name__)

#  Venues
#  ----------------------------------------------------------------


class VenueController:
    @venue_blueprint.route("/")
    def venues():
        # TODO: replace with real venues data.
        #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        # {"id": venue.id, "name": venue.name, "num_upcoming_shows": len([])}
        data = []
        res_data = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
        for d in res_data:
            venues_list = []
            venues_query = (
                Venue.query.filter_by(city=d.city).filter_by(state=d.state).all()
            )
            for venue in venues_query:
                venues_list.append(
                    {"id": venue.id, "name": venue.name, "num_upcoming_shows": len([])}
                )
            data.append({"city": d.city, "state": d.state, "venues": venues_list})

        return render_template("pages/venues.html", areas=data)

    @venue_blueprint.route("/search", methods=["POST"])
    def search_venues():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        search_term = request.form.get("search_term")
        search_term = "%{}%".format(search_term)
        res_Name = Venue.name.ilike(search_term)
        res_City = Venue.city.ilike(search_term)
        res_State = Venue.state.ilike(search_term)
        query_data = Venue.query.filter(res_Name | res_City | res_State).all()
        data = []
        for d in query_data:
            data.append({"id": d.id, "name": d.name, "num_upcoming_shows": 0})
        response = {"count": len(query_data), "data": data}
        print(response)
        return render_template(
            "pages/search_venues.html",
            results=response,
            search_term=request.form.get("search_term", ""),
        )

    @venue_blueprint.route("/<int:venue_id>")
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # avoid all then try .first() instead else search for single retrieval on the web
        venue = Venue.query.filter_by(id=venue_id).first()
        # TODO: replace with real venue data from the venues table, using venue_id
        past_shows = []
        upcoming_shows = []
        for v in venue.shows:
            res_data = {
                "artist_id": v.artist_id,
                "artist_name": v.artist.name,
                "artist_image_link": v.artist.image_link,
                "start_time": v.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            if datetime.now() > v.start_time:
                past_shows.append(res_data)
            else:
                upcoming_shows.append(res_data)

        data1 = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
        # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
        return render_template("pages/show_venue.html", venue=data1)

    #  Create Venue
    #  ----------------------------------------------------------------
    # @tshirts_bluepirnt.route("/edit",methods=["GET"])
    @venue_blueprint.route("/create", methods=["GET"])
    def create_venue_form():
        form = VenueForm()
        return render_template("forms/new_venue.html", form=form)

    @venue_blueprint.route("/create", methods=["POST"])
    def create_venue_submission():
        # TODO: insert form data as a new Venue record in the db, instead
        # TODO: modify data to be the data object returned from db insertion
        error = False
        try:
            name = request.form["name"]
            city = request.form["city"]
            state = request.form["state"]
            address = request.form["address"]
            genres = request.form.getlist("genres")
            phone = request.form["phone"]
            image_link = request.form["image_link"]
            facebook_link = request.form["facebook_link"]
            website = request.form["website"]
            seeking_talent = bool(request.form["seeking_talent"])
            seeking_description = request.form["seeking_description"]
            created_at = datetime.now()
            venue = Venue(
                name=name,
                city=city,
                state=state,
                address=address,
                phone=phone,
                genres=genres,
                facebook_link=facebook_link,
                image_link=image_link,
                website=website,
                seeking_talent=seeking_talent,
                seeking_description=seeking_description,
                created_at=created_at,
            )

            db.session.add(venue)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        # on successful db insert, flash success
        if not error:
            flash("Venue " + request.form["name"] + " was successfully listed!")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        if error:
            flash("An error occurred. Venue " + Venue.name + "could not be listed")
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template("pages/home.html")

    # deleting
    @venue_blueprint.route("/<venue_id>", methods=["DELETE"])
    def delete_venue(venue_id):
        # TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        error = False
        try:
            venues = Venue.query.get(venue_id)
            # TODO: delete related shows before deleting the venue
            db.session.delete(venues)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if not error:
            flash("Venue was successfully deleted.")
        if error:
            flash(f"An error occurred.")

        return redirect(url_for("home.index"))

    #  Update Venue
    #  ----------------------------------------------------------------
    @venue_blueprint.route("/<int:venue_id>/edit", methods=["GET"])
    def edit_venue(venue_id):
        form = VenueForm()
        #  venue={
        #     "id": 1,
        #     "name": "The Musical Hop",
        #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        #     "address": "1015 Folsom Street",
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "phone": "123-123-1234",
        #     "website": "https://www.themusicalhop.com",
        #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
        #     "seeking_talent": True,
        #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        #   }
        venue = Venue.query.filter_by(id=venue_id).first()

        form.seeking_talent.default = venue.seeking_talent
        form.process()

        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.genres.data = venue.genres
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.website.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.seeking_description.data = venue.seeking_description

        # TODO: populate form with values from venue with ID <venue_id>
        return render_template("forms/edit_venue.html", form=form, venue=venue)

    @venue_blueprint.route("/<int:venue_id>/edit", methods=["POST"])
    def edit_venue_submission(venue_id):
        # TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        venues = Venue.query.get(venue_id)
        error = False
        try:
            venues.name = request.form["name"]
            venues.city = request.form["city"]
            venues.state = request.form["state"]
            venues.address = request.form["address"]
            venues.genres = request.form.getlist("genres")
            venues.phone = request.form["phone"]
            venues.image_link = request.form["image_link"]
            venues.facebook_link = request.form["facebook_link"]
            venues.website = request.form["website"]
            venues.seeking_talent = json.loads(request.form["seeking_talent"].lower())
            venues.seeking_description = request.form["seeking_description"]

            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if not error:
            flash("Venue " + request.form["name"] + " was successfully listed!")
        if error:
            flash("An error occurred.")
        return redirect(url_for("venues.show_venue", venue_id=venue_id))
