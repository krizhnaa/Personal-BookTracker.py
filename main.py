from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import os
from dotenv import find_dotenv, load_dotenv
import requests

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  os.getenv("dburl")
app.config['SECRET_KEY'] = os.getenv("sk")
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


class Editform(FlaskForm):
    rating = FloatField('Rating Out of 10', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Addform(FlaskForm):
    book = StringField('Which Book to add?', validators=[DataRequired()])
    submit = SubmitField('Submit')


def search_book(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}&maxResults=1"
    response = requests.get(url)
    data = response.json()
    if "items" in data and data["items"]:
        book_info = data["items"][0]["volumeInfo"]
        book_title = book_info.get("title", "Title not available")
        authors = book_info.get("authors", ["Author not available"])
        author = authors[0] if authors else "Author not available"
        year = book_info.get("publishedDate", "Year not available")
        img_url = book_info.get("imageLinks", {}).get("thumbnail", "Image URL not available")
        return {
            "title": book_title,
            "author": author,
            "year": year,
            "img_url": img_url
        }
    else:
        return None


@app.route("/")
def home():
    books = BookCollection.query.order_by(BookCollection.rating.desc()).all()
    for i, book in enumerate(books):
        book.ranking = i + 1
    return render_template("index.html", db=books)


@app.route("/edit/<bookname>", methods=['GET', 'POST'])
def edit(bookname):
    form = Editform()
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data
        with app.app_context():
            book = BookCollection.query.filter_by(title=bookname).first()
            book.rating = rating
            book.description = review
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form)


@app.route("/deleting/<bookname>")
def delete(bookname):
    with app.app_context():
        book = BookCollection.query.filter_by(title=bookname).first()
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = Addform()
    if form.validate_on_submit():
        searchname = form.book.data
        book_info = search_book(searchname)
        with app.app_context():
            id_count = db.session.query(db.func.max(BookCollection.id)).scalar()
            rank_count = db.session.query(db.func.max(BookCollection.ranking)).scalar()
            if book_info["year"] == "Year not available":
                book_info["year"] = "00000"
            print(id_count)
            if id_count == None:
                id_count = 0
            data = BookCollection(id=id_count + 1,
                                  title=book_info["title"],
                                  year=int(book_info["year"][:4]),
                                  description="Null",
                                  author=book_info["author"],
                                  rating=0,
                                  ranking=rank_count + 1,
                                  img_url=book_info["img_url"]
                                  )
            db.session.add(data)
            db.session.commit()
        return redirect(url_for('edit', bookname=book_info["title"]))
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
