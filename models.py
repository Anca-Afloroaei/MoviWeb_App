from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Float, ForeignKey, Integer, String


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', backref='user', cascade="all, delete-orphan")


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
