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
    rating = db.Column(db.Float, unique=False, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(100), unique=True, nullable=False)


# with app.app_context():
#     id_count = db.session.query(db.func.max(BookCollection.id)).scalar()
#     print(id_count)
#     if id_count == None:
#         id_count = 0
#     data = BookCollection(id=id_count + 1,
#                           title="Zen: The Art of Simple Living",
#                           year=2019,
#                           description="This book explores the principles of Zen philosophy and how they can be applied to everyday life to achieve simplicity, clarity, and inner peace. It offers practical wisdom and guidance on various aspects of life, including mindfulness, minimalism, and living in the present moment.",
#                           author="Shunmyo Masuno",
#                           rating=8.5,
#                           ranking=9,
#                           img_url="https://m.media-amazon.com/images/I/41rkNNOWURL.jpg"
#                           )
#     db.session.add(data)
#     db.session.commit()


@app.route("/")
def home():
    dbms = BookCollection.query.all()
    return render_template("index.html", db=dbms)


if __name__ == '__main__':
    app.run(debug=True)
