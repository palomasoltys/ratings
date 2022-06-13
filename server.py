"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ Homepage view function"""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """Display all movies."""   

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies) 


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():
    """Show all users"""
    users = crud.get_users()

    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show users profile."""

    user = crud.get_user_by_id(user_id)
    
    return render_template("user_profile.html", user=user)

@app.route('/users', methods=['POST'])
def register_user():
    """Create new user"""
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    user = crud.get_user_by_email(user_email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(user_email, user_password)
        db.session.add(user)    
        db.session.commit()
        flash('Account created! Please, log in.')


    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    """ Show loggged in page """

    user_email = request.form.get("email")
    user_password = request.form.get("password")

    user_info = crud.User.query.filter_by(email=user_email).first()

    if user_info and user_info.password == user_password:
        flash("Logged in!")
        session['user_id'] = user_info.user_id
        return redirect('/movies')

    else:
        flash("User email or password don't match. Try again.")

    return redirect('/')

@app.route('/movies/<movie_id>/rating', methods=['POST'])   
def get_rating(movie_id):

    if 'user_id' in session:
        score = request.form.get("rating") 
        movie = crud.get_movie_by_id(movie_id)
        user = crud.get_user_by_id(session['user_id'])
        rating = crud.Rating(score=score, movie=movie, user=user)
        db.session.add(rating)
        db.session.commit()
    else:
        return redirect('/')    
    return redirect('/movies')    


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
