from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float
import secrets


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
app.secret_key = secrets.token_hex(32)

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __init__(self, title: str, author: str, rating: float) -> None:
        self.title = title
        self.author = author
        self.rating = rating


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        rating = request.form.get("rating", "").strip()
        if title and author and rating:
            book = Book(title=title, author=author, rating=float(rating))
            db.session.add(book)
            db.session.commit()
            flash(f'"{title}" added successfully!', "success")
            return redirect(url_for("home"))
        flash("All fields are required.", "danger")
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id: int):
    book = db.get_or_404(Book, book_id)
    if request.method == "POST":
        book.title = request.form.get("title", "").strip()
        book.author = request.form.get("author", "").strip()
        rating = request.form.get("rating", "").strip()
        if not (book.title and book.author and rating):
            flash("All fields are required.", "danger")
            return render_template("edit.html", book=book)
        book.rating = float(rating)
        db.session.commit()
        flash(f'"{book.title}" updated successfully!', "success")
        return redirect(url_for("home"))
    return render_template("edit.html", book=book)


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id: int):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'"{book.title}" deleted.', "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)



