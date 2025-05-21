from flask import Flask, redirect, render_template, request, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie
import os



app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'moviwebapp.db')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviwebapp.db"

data_manager = SQLiteDataManager(app)



@app.route('/')
def home():
    """ the home page of our application """
    return render_template('home.html')    #"Welcome to MovieWeb App!"


@app.route('/users', methods=['GET'])
def list_users():
    """ presents a list of all users """
    users = data_manager.get_all_users()
    #return str(users)  # Temporarily returning users as a string
    return render_template('users.html', users=users)


@app.route('/users/<user_id>', methods=['GET'])
def list_user_movies(user_id):
    """ shows a specific user’s list of favorite movies """
    #movies = data_manager.get_user_movies(user_id)
    #return movies
    user = User.query.get_or_404(user_id)
    return render_template('user_movies.html', user=user, movies=user.movie)


@app.route('/add_user', methods=['GET', 'POST'])
def add_users():
    """ allows the additions of new users """
    if request.method == 'POST':
        user_name = request.form.get('name')
        try:
            new_user = User(name=user_name)
            data_manager.add_user(new_user)
            return redirect(url_for('user_movies', user_id=new_user.id))
        except Exception as e:
            print(f"Failed to add user: {e}")

    return render_template('add_user.html')


    # return '''
    #     <form method="post">
    #         <label>Name:</label>
    #         <input name="name" type="text">
    #         <input type="submit" value="Add User">
    #     </form>
    # '''


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """ allows the additions of new movies """
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        #user_id = request.form.get('user_id')
        try:
            new_movie = Movie(
                title=title,
                director=director,
                 year=year,
                 rating=rating,
                 user_id=user_id
            )

            #movie = Movie(title=title, user_id=user_id)
            data_manager.add_movie(new_movie)
            return redirect(url_for('list_user_movies', user_id=user_id))

            #return render_template('message.html', message="Movie added!")
        except Exception as e:
            print(f"Failed to add movie: {e}")
            return render_template('message.html', message="Failed to add movie.", user_id=user_id)

    return render_template('add_movie.html', user=user)

    # return '''
    #     <form method="post">
    #         <label>Title:</label>
    #         <input title="title" type="text">
    #         <input type="submit" value="Add Movie">
    #     </form>
    # '''



@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """ allows updates for a movie """
    if request.method == 'POST':
        title = request.form.get('title')
        movie = Movie(title=title, user_id=user_id, movie_id=movie_id)
        data_manager.update_movie(movie)

    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id)

    # return '''
    #     <form method="post">
    #         <label>New Rating:</label>
    #         <input rating="rating" type="number">
    #         <input type="submit" value="Updated rating for movie {title}">
    #     </form>
    # '''


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """ allows updates for a movie """
    # title = request.form.get('title')
    # movie = Movie(title=title, user_id=user_id, movie_id=movie_id)
    data_manager.delete_movie(movie_id)

    return render_template('message.html', message=f"Movie {movie_id} deleted for User {user_id}!")





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)