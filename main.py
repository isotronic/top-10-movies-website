from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
import requests
import os

API_KEY = os.environ["API_KEY"]
ACCESS_TOKEN = os.environ["API_READ_ACCESS_TOKEN"]

# Initialize the Flask app and set the app's configurations
db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-10-movies.db"
db.init_app(app)
Bootstrap5(app)


# Define FlaskForm classes for rating and adding movies
class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating out of 10, e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    movie_id = HiddenField()
    submit = SubmitField("Save")


class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# Define the Movie class to represent the database table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String)


# Fetch all movies from the database and order them by rating in descending order
@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
        result_scalar = result.scalars()
        all_movies = [r for r in result_scalar]

    # Update the rankings of movies based on their order in the sorted list
    new_ranking = 1
    for movie in all_movies:
        movie.ranking = new_ranking
        with app.app_context():
            movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == movie.title)).scalar()
            movie_to_update.ranking = movie.ranking
            db.session.commit()
        new_ranking += 1
    return render_template("index.html", movies=all_movies)


# Define the route for editing the rating and review of a movie
@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    form = RateMovieForm()
    if form.validate_on_submit():
        # Update the rating and review of the movie in the database
        movie_id = form.movie_id.data
        with app.app_context():
            movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
            movie_to_update.rating = form.rating.data
            movie_to_update.review = form.review.data
            db.session.commit()
        return redirect(url_for("home"))

    # Get the movie ID from the request arguments and populate the form
    movie_id = request.args.get("id", type=int)
    form.movie_id.data = movie_id
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    return render_template("edit.html", form=form, movie=movie_to_update)


# Define the route for deleting a movie
@app.route("/delete", methods=["GET"])
def delete_movie():
    movie_id = request.args.get("id", type=int)
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for("home"))


# Define the route for adding a new movie
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        url = f"https://api.themoviedb.org/3/search/movie?query={form.title.data}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        movies_found = response.json()["results"]
        return render_template("select.html", movies=movies_found)

    # Get the movie details from the request arguments and add the movie to the database
    moviedb_id = request.args.get("movie_id", type=int)
    release_date = request.args.get("release_date")
    if moviedb_id:
        url = f"https://api.themoviedb.org/3/movie/{moviedb_id}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)

        new_movie = Movie(
            title=response.json()["original_title"],
            year=release_date.split("-")[0],
            description=response.json()["overview"],
            img_url=f"https://image.tmdb.org/t/p/w500{ response.json()['poster_path'] }"
        )

        with app.app_context():
            db.session.add(new_movie)
            db.session.commit()

        with app.app_context():
            movie_id = db.session.execute(db.select(Movie).where(Movie.title == response.json()["original_title"])).scalar().id

        return redirect(url_for("edit_rating", id=movie_id))

    return render_template("add.html", form=form)


# Run the Flask app in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
