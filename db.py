from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from config import DB_URI

current_app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(current_app)
migrate = Migrate(current_app, db) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)
    rentals = db.relationship('Rental', backref='user')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(30))
    publisher = db.Column(db.String(30))
    publication_date = db.Column(db.Date)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.String(50))
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    image = db.Column(db.String(50))
    rating = db.Column(db.Integer, default=0)
    available = db.Column(db.Integer, default=5)


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    rental_date = db.Column(db.Date, default=(datetime.now()+timedelta(hours=9)).date())
    return_date = db.Column(db.Date)
    book_detail = db.relationship('Book')


def init_db():
    # bind db and app
    db.init_app(current_app)
    db.create_all()
