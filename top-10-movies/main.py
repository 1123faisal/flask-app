from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Text
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TMDB_API_KEY = "15551e816d6f5bcb92c24c9f4921daa7"   # replace with your key from themoviedb.org
TMDB_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

_retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
_adapter = HTTPAdapter(max_retries=_retry)
tmdb_session = requests.Session()
tmdb_session.headers.update(TMDB_HEADERS)
tmdb_session.mount("https://", _adapter)


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ── Model ──────────────────────────────────────────────────────────────────────
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(500), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)

    def __init__(self, title: str, year: int, description: str, img_url: str,
                 rating: float = 0.0, ranking: int = 0, review: str = "") -> None:
        self.title = title
        self.year = year
        self.description = description
        self.img_url = img_url
        self.rating = rating
        self.ranking = ranking
        self.review = review


# ── Forms ──────────────────────────────────────────────────────────────────────
class RateMovieForm(FlaskForm):
    rating = FloatField("Your Rating (out of 10)", validators=[DataRequired(), NumberRange(0, 10)])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Search")


# ── Seed data ──────────────────────────────────────────────────────────────────
SEED_MOVIES = [
    {"title": "The Dark Knight", "year": 2008, "rating": 9.0, "ranking": 1,
     "review": "Best superhero film ever made.",
     "img_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
     "description": "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations."},
    {"title": "Inception", "year": 2010, "rating": 8.8, "ranking": 2,
     "review": "Mind-bending masterpiece.",
     "img_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
     "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."},
    {"title": "Interstellar", "year": 2014, "rating": 8.6, "ranking": 3,
     "review": "Visually stunning and emotionally deep.",
     "img_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
     "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"title": "The Matrix", "year": 1999, "rating": 8.7, "ranking": 4,
     "review": "Changed sci-fi forever.",
     "img_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
     "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."},
    {"title": "Pulp Fiction", "year": 1994, "rating": 8.9, "ranking": 5,
     "review": "Tarantino at his finest.",
     "img_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
     "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
    {"title": "Parasite", "year": 2019, "rating": 8.6, "ranking": 6,
     "review": "A flawless thriller with a savage twist.",
     "img_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
     "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."},
    {"title": "Whiplash", "year": 2014, "rating": 8.5, "ranking": 7,
     "review": "Intense, gripping, unforgettable.",
     "img_url": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
     "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are challenged by an instructor who will stop at nothing."},
    {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "ranking": 8,
     "review": "Hope is a good thing.",
     "img_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
     "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    {"title": "Drive", "year": 2011, "rating": 7.8, "ranking": 9,
     "review": "Stylish and cool with a great soundtrack.",
     "img_url": "https://image.tmdb.org/t/p/w500/602vevIURmpDfzbnv5Ubi6wIkQm.jpg",
     "description": "A mysterious Hollywood stuntman and mechanic moonlights as a getaway driver and finds himself in trouble when he helps out his neighbor."},
    {"title": "Phone Booth", "year": 2002, "rating": 7.3, "ranking": 10,
     "review": "My favourite character was the caller.",
     "img_url": "https://image.tmdb.org/t/p/w500/r6lIwPKVDa6Q76qH2TbIBqPhXL3.jpg",
     "description": "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle."},
]

with app.app_context():
    db.create_all()
    # Patch any already-seeded rows that have broken poster URLs
    _poster_fixes = {
        "Drive": "https://image.tmdb.org/t/p/w500/602vevIURmpDfzbnv5Ubi6wIkQm.jpg",
        "Phone Booth": "https://image.tmdb.org/t/p/w500/r6lIwPKVDa6Q76qH2TbIBqPhXL3.jpg",
    }
    for _title, _url in _poster_fixes.items():
        _movie = db.session.execute(db.select(Movie).filter_by(title=_title)).scalar_one_or_none()
        if _movie and _movie.img_url != _url:
            _movie.img_url = _url
    db.session.commit()
    # Assign rankings to any movies that have ranking=0 (added before the fix)
    _unranked = db.session.execute(db.select(Movie).filter_by(ranking=0)).scalars().all()
    if _unranked:
        _max_ranking = db.session.execute(
            db.select(db.func.max(Movie.ranking)).where(Movie.ranking > 0)
        ).scalar_one_or_none() or 0
        for _m in _unranked:
            _max_ranking += 1
            _m.ranking = _max_ranking
        db.session.commit()
    if Movie.query.count() == 0:
        for m in SEED_MOVIES:
            db.session.add(Movie(**m))
        db.session.commit()
    # Always re-rank on startup so rankings match rating order
    _all = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()
    for _i, _m in enumerate(_all, start=1):
        _m.ranking = _i
    db.session.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────
def rerank_movies():
    """Re-assign rankings to all movies ordered by rating descending."""
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    ).scalars().all()
    for i, m in enumerate(movies, start=1):
        m.ranking = i
    db.session.commit()


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", movies=movies)


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id: int):
    movie = db.get_or_404(Movie, movie_id)
    form = RateMovieForm(obj=movie)
    if form.validate_on_submit():
        if form.rating.data is not None:
            movie.rating = form.rating.data
        if form.review.data is not None:
            movie.review = form.review.data
        db.session.commit()
        rerank_movies()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id: int):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    rerank_movies()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        # Search TMDB
        resp = tmdb_session.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_API_KEY, "query": title},
            timeout=10,
        )
        results = resp.json().get("results", [])
        return render_template("select.html", movies=results)
    return render_template("add.html", form=form)


@app.route("/add/select/<int:tmdb_id>")
def add_select(tmdb_id: int):
    resp = tmdb_session.get(
        f"https://api.themoviedb.org/3/movie/{tmdb_id}",
        params={"api_key": TMDB_API_KEY},
        timeout=10,
    )
    data = resp.json()
    movie = Movie(
        title=data["title"],
        year=int(data["release_date"][:4]),
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for("edit", movie_id=movie.id))


if __name__ == '__main__':
    app.run(debug=True)

