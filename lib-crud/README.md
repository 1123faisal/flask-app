# Library CRUD

Simple Flask CRUD application to manage a book collection with SQLite.

## Features

- View all books
- Add a new book
- Edit title, author, and rating
- Delete books
- Flash messages for user feedback

## Stack

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- SQLite

## Run Locally

```bash
uv sync
uv run python main.py
```

Alternative:

```bash
pip install -r requirements.txt
python main.py
```

Open http://127.0.0.1:5000

## Notes

- Database is auto-created as `books-collection.db`.
