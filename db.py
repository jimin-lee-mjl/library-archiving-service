from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from config import DB_URI

current_app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(current_app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)


def init_db():
    # bind db and app
    db.init_app(current_app)
    db.drop_all()
    db.create_all()