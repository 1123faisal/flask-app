from dataclasses import dataclass
from datetime import date

from flask import Blueprint, abort, render_template

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@dataclass(frozen=True)
class Movie:
    slug: str
    title: str
    director: str
    year: int
    runtime: str
    rating: int
    status: str
    watched_on: str
    tags: list[str]
    cast: list[str]
    series: str
    description: str
    video_link: str
    accent: str


MOVIES = [
    Movie(
        slug="the-matrix",
        title="The Matrix",
        director="Lana and Lilly Wachowski",
        year=1999,
        runtime="136 min",
        rating=5,
        status="Rewatch queued",
        watched_on="24 Mar 2022",
        tags=["Sci-fi", "Action"],
        cast=["Keanu Reeves", "Carrie-Anne Moss", "Laurence Fishburne", "Hugo Weaving"],
        series="The Matrix Saga",
        description=(
            "A hacker discovers the world is a simulation and decides to fight the system that built it."
        ),
        video_link="https://www.youtube.com/embed/9ix7TUGVYIo",
        accent="matrix",
    ),
    Movie(
        slug="spirited-away",
        title="Spirited Away",
        director="Hayao Miyazaki",
        year=2001,
        runtime="125 min",
        rating=5,
        status="Watched and loved",
        watched_on="08 Jan 2024",
        tags=["Fantasy", "Animation"],
        cast=["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
        series="Studio Ghibli Essentials",
        description=(
            "A young girl enters a spirit world and navigates wonder, danger, and courage to save her family."
        ),
        video_link="https://www.youtube.com/embed/ByXuk9QqQkk",
        accent="sunset",
    ),
    Movie(
        slug="arrival",
        title="Arrival",
        director="Denis Villeneuve",
        year=2016,
        runtime="116 min",
        rating=4,
        status="Watch again",
        watched_on="12 Feb 2025",
        tags=["Drama", "Sci-fi"],
        cast=["Amy Adams", "Jeremy Renner", "Forest Whitaker"],
        series="First Contact",
        description=(
            "A linguist works to communicate with alien visitors, changing humanity's understanding of time."
        ),
        video_link="https://www.youtube.com/embed/tFMo3UJ4B4g",
        accent="copper",
    ),
]


@pages.context_processor
def inject_globals() -> dict[str, int | str]:
    watched_count = len(MOVIES)
    average_rating = round(sum(movie.rating for movie in MOVIES) / watched_count, 1)
    return {
        "current_year": date.today().year,
        "watched_count": watched_count,
        "average_rating": str(average_rating),
    }


@pages.get("/")
def home() -> str:
    featured = MOVIES[0]
    recent_movies = MOVIES
    return render_template("home.html", featured=featured, recent_movies=recent_movies)


@pages.get("/login")
def login() -> str:
    return render_template("login.html")


@pages.get("/signup")
def signup() -> str:
    return render_template("signup.html")


@pages.get("/movies")
def movies() -> str:
    return render_template("movies.html", movies=MOVIES)


@pages.get("/movies/new")
def new_movie() -> str:
    return render_template("movie_form.html", movie=MOVIES[0])


@pages.get("/movies/<slug>")
def movie_detail(slug: str) -> str:
    movie = next((item for item in MOVIES if item.slug == slug), None)
    if movie is None:
        abort(404)
    related_movies = [item for item in MOVIES if item.slug != slug][:2]
    return render_template(
        "movie_detail.html", movie=movie, related_movies=related_movies
    )
