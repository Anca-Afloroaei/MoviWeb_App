from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie
import os
import requests
from config import OMDB_API_KEY



app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'moviwebapp.db')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviwebapp.db" # is it doesn't work remove instance

#db.init_app(app)

#load_dotenv()   # I have it in config.py

data_manager = SQLiteDataManager(app)



@app.route('/')
def home():
    """ the home page of our application """
    return render_template('home.html')    #"Welcome to MovieWeb App!"


@app.route('/users', methods=['GET'])
def list_users():
    """ presents a list of all users """
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
        #return str(users)  # Temporarily returning users as a string
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return render_template('message.html', message="Failed to retrieve the users.")

    #return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def list_user_movies(user_id):
    """ shows a specific user’s list of favorite movies """
    #movies = data_manager.get_user_movies(user_id)
    #return movies
    try:
        user = User.query.get_or_404(user_id)
        #return render_template('user_movies.html', user=user)
        return render_template('user_movies.html', user=user, movies=user.movies)
    except Exception as e:
        print(f"Error retrieving movies: {e}")
        return render_template('message.html', message="Failed to retrieve the movies.")


@app.route('/add_user', methods=['GET', 'POST'])
def add_users():
    """ allows the additions of new users """
    if request.method == 'POST':
        user_name = request.form.get('name')
        try:
            new_user = User(name=user_name)
            data_manager.add_user(new_user)
            return redirect(url_for('list_user_movies', user_id=new_user.id))
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
    api_key = os.getenv("API_KEY")

    if request.method == 'POST':
        title = request.form.get('title')
        rating = float(request.form.get('rating'))

        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        # params = {
        #     "t": title,
        #     "apikey": api_key
        # }
        #response = requests.get(url, params=params)

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data.get("Response") != "False":
                try:
                    new_movie = Movie(
                        title=data.get("Title", title),
                        director=data.get("Director", "Unknown"),
                        year=int(data.get("Year", 0)),
                        rating=rating,
                        user_id=user_id
                    )

                    data_manager.add_movie(new_movie)
                    return redirect(url_for('list_user_movies', user_id=user_id))

                except Exception as e:
                    print(f"Failed to add movie: {e}")
                    return render_template('message.html', message="Failed to add movie.", user_id=user_id)

            else:
                return render_template('message.html', message="Failed to add movie. Movie not found", user_id=user_id)

        else:
            return render_template('message.html', message="Error connecting to the OMDb API", user_id=user_id)

    return render_template('add_movie.html', user=user)












    #     director = request.form.get('director')
    #     year = request.form.get('year')
    #     rating = request.form.get('rating')
    #
    #     #user_id = request.form.get('user_id')
    #     try:
    #         new_movie = Movie(
    #             title=title,
    #             director=director,
    #              year=year,
    #              rating=rating,
    #              user_id=user_id
    #         )
    #
    #         #movie = Movie(title=title, user_id=user_id)
    #         data_manager.add_movie(new_movie)
    #         return redirect(url_for('list_user_movies', user_id=user_id))
    #
    #         #return render_template('message.html', message="Movie added!")
    #     except Exception as e:
    #         print(f"Failed to add movie: {e}")
    #         return render_template('message.html', message="Failed to add movie.", user_id=user_id)
    #
    # return render_template('add_movie.html', user=user)

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
    user = User.query.get_or_404(user_id) # added for API
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        try:
            new_title = request.form.get('title') # added for API
            new_rating = request.form.get('rating')

            if new_title:
                movie.title = new_title
            if new_rating:
                movie.rating = float(new_rating)
            db.session.commit()
            #data_manager.update_movie(movie)
            # movie.title = request.form.get('title')
            # movie.director = request.form.get('director')
            # movie.year = request.form.get('year')
            # movie.rating = request.form.get('rating')
            # movie.title = request.form.get('title')
            # movie.director = request.form.get('director')
            # movie.year = request.form.get('year')
            # #movie.rating = request.form.get('rating')
            # movie.user_id = request.form.get('user_id')


            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            print(f"Failed to update movie: {e}")
            return render_template('message.html', message="Failed to update movie.")



    return render_template('update_movie.html', movie=movie, user_id=user_id)

    # return '''
    #     <form method="post">
    #         <label>New Rating:</label>
    #         <input rating="rating" type="number">
    #         <input type="submit" value="Updated rating for movie {title}">
    #     </form>
    # '''


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """ Deletes a movie and returns a message. """
    # title = request.form.get('title')
    # movie = Movie(title=title, user_id=user_id, movie_id=movie_id)
    #data_manager.delete_movie(movie_id)
    movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
    
    if movie:
        try:
            db.session.delete(movie)
            db.session.commit()
            return render_template('message.html', message=f"Movie {movie.title} deleted for user {user_id}!",
                                   user_id=user_id)
        except Exception as e:
            db.session.rollback()
            print(f"Failed to delete movie: {e}")
            return render_template('message.html', message="Failed to delete movie.", user_id=user_id)
    else:
        return render_template('message.html', message="Movie not found.", user_id=user_id)

    
    

    #return render_template('message.html', message=f"Movie {movie_id} deleted for User {user_id}!")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)