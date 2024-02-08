from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
db = SQLAlchemy(app)


# CREATE DB
class BookCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)
    author = db.Column(db.String(30), unique=False, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    img_url = db.Column(db.String(100), unique=True, nullable=False)


# CREATE TABLE
with app.app_context():
    db.create_all()



# @app.route("/")
# def home():
#     return render_template("index.html")
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
