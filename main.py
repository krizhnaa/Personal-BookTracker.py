from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


class NewBookCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(30), unique=True, nullable=False)
    author = db.Column(db.String(30), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        bookname = request.form.get('bookname')
        author = request.form.get('author')
        rating = float(request.form.get('rating'))
        with app.app_context():
            id_count = db.session.query(db.func.max(NewBookCollection.id)).scalar()
            print(id_count)
            if id_count == None:
                id_count = 0
            data = NewBookCollection(id=id_count+1, book=bookname, author=author, rating=rating)
            db.session.add(data)
            db.session.commit()
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

