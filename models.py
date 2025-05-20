from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey("user.id"))
    title = db.Column(String)
    director = db.Column(String)
    year = db.Column(Integer)
    rating = db.Column(Float)
