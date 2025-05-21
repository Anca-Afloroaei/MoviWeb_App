from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)
    movie = db.relationship('Movie', backref='user', cascade="all, delete-orphan")


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey("users.id"), nullable=False)
    title = db.Column(String)
    director = db.Column(String)
    year = db.Column(Integer)
    rating = db.Column(Float)
