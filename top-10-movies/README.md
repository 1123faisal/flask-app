# Top 10 Movies

Flask web app to manage a ranked movie list with ratings, reviews, and TMDB search integration.

## Features

- Home page with ranked movie list
- Add movies by searching TMDB
- Edit rating and review
- Delete movies
- Automatic ranking based on rating

## Stack

- Python 3.12+
- Flask
- Flask-WTF
- Flask-Bootstrap
- Flask-SQLAlchemy
- Requests
- SQLite

## Configuration

- Update `TMDB_API_KEY` in `main.py` with your own key from themoviedb.org.

## Run Locally

```bash
uv sync
uv run python main.py
```

Alternative:

```bash
pip install flask flask-bootstrap flask-wtf flask-sqlalchemy requests
python main.py
```

Open http://127.0.0.1:5000

## Notes

- Database `movies.db` is created automatically.
- Initial seed data is added when database is empty.
