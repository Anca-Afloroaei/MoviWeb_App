from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datamanager.data_manager_interface import DataManagerInterface
from models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        """ Set up the database with the Flask app """
        #self.db = SQLAlchemy(db_file_name)
        self.app = app
        db.init_app(app)  # Connect db to app
        with app.app_context():
            db.create_all()  # Create tables if they don’t exist yet



    # def __init__(self, app):
    #     """
    #     Set up the database with the Flask app.
    #     This connects SQLAlchemy to your Flask app and creates all the tables.
    #     """
    #     self.app = app
    #     db.init_app(app)  # Connect db to app
    #     with app.app_context():
    #         db.create_all()  # Create tables if they don’t exist yet



    def get_all_users(self):
        """ docstring """
        return User.query.all()


    def get_user_movies(self, user_ID):
        """ docstring """
        return Movie.query.filter_by(user_id=user_ID).all()


    def add_user(self, user):
        """ docstring """
        try:
            db.session.add(user)
            db.session.commit()
            print(f"User '{user}' added successfully!")
        except Exception as e:from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datamanager.data_manager_interface import DataManagerInterface
from models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        """ Set up the database with the Flask app """
        #self.db = SQLAlchemy(db_file_name)
        self.app = app
        db.init_app(app)  # Connect db to app
        with app.app_context():
            db.create_all()  # Create tables if they don’t exist yet



    # def __init__(self, app):
    #     """
    #     Set up the database with the Flask app.
    #     This connects SQLAlchemy to your Flask app and creates all the tables.
    #     """
    #     self.app = app
    #     db.init_app(app)  # Connect db to app
    #     with app.app_context():
    #         db.create_all()  # Create tables if they don’t exist yet



    def get_all_users(self):
        """ docstring """
        return User.query.all()


    def get_user_movies(self, user_ID):
        """ docstring """
        return Movie.query.filter_by(user_id=user_ID).all()


    def add_user(self, user):
        """ docstring """
        try:
            db.session.add(user)
            db.session.commit()
            print(f"User '{user}' added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add user: {str(e)}")



    def add_movie(self, movie):
        """ docstring """

        #user = User.query.all()

        try:
            db.session.add(movie)
            db.session.commit()
            print(f"Movie '{movie.title}' added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add movie: {str(e)}")

        #return render_template('add_book.html', authors=authors)


    def update_movie(self, movie):
        """ docstring """
        movie = Movie.query.get_or_404(id)
        title = movie.title

        if request.method == 'POST':

            movie.title = request.form.get('title')
            movie.director = request.form.get('director')
            movie.year = request.form.get('year')
            movie.rating = request.form.get('rating')
            movie.user_id = request.form.get('user_id')

            try:
                db.session.commit()
                print(f"Movie '{movie.title}' updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to update movie: {str(e)}")

        #return render_template('add_book.html', authors=authors)



    def delete_movie(self, movie):
        """ docstring """
        """This function deletes a book, and deletes its author if the author has no other books."""
        movie = Movie.query.get_or_404(id)
        title = movie.title
        user = movie.user_id

        try:
            db.session.delete(movie)
            db.session.commit()

            # Check if user has any other movies
            other_movies = Movie.query.filter_by(user_id=user.id).count()
            if other_movies == 0:
                db.session.delete(user)
                db.session.commit()

            print(f"Deleted movie '{title}' successfully.")
            #return redirect(f"/?deleted={title}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting movie: {str(e)}")
            #return redirect("/")

            db.session.rollback()
            print(f"Failed to add user: {str(e)}")



    def add_movie(self, movie):
        """ docstring """

        user = User.query.all()

        if request.method == 'POST':

            title = request.form.get('title')
            director = request.form.get('director')
            year = request.form.get('year')
            rating = request.form.get('rating')
            user_id = request.form.get('user_id')
            new_movie = Movie(
                title=title,
                director=director,
                year=year,
                rating=rating,
                user_id=user_id
            )

            try:
                db.session.add(movie)
                db.session.commit()
                print(f"Movie '{movie.title}' added successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to add movie: {str(e)}")

        #return render_template('add_book.html', authors=authors)


    def update_movie(self, movie):
        """ docstring """
        movie = Movie.query.get_or_404(movie.id)
        title = movie.title

        if request.method == 'POST':

            movie.title = request.form.get('title')
            movie.director = request.form.get('director')
            movie.year = request.form.get('year')
            movie.rating = request.form.get('rating')
            movie.user_id = request.form.get('user_id')

            try:
                db.session.commit()
                print(f"Movie '{movie.title}' updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to update movie: {str(e)}")

        #return render_template('add_book.html', authors=authors)



    def delete_movie(self, movie):
        """ docstring """
        """This function deletes a book, and deletes its author if the author has no other books."""
        movie = Movie.query.get_or_404(id)
        title = movie.title
        user = movie.user_id

        try:
            db.session.delete(movie)
            db.session.commit()

            # Check if user has any other movies
            other_movies = Movie.query.filter_by(user_id=user.id).count()
            if other_movies == 0:
                db.session.delete(user)
                db.session.commit()

            print(f"Deleted movie '{title}' successfully.")
            #return redirect(f"/?deleted={title}")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting movie: {str(e)}")
            #return redirect("/")
