# Flask Auth Start

Starter Flask authentication app with secure login flow, registration, protected routes, and downloadable protected file access.

## Features

- User registration and login
- Password hashing
- Session-based authentication with Flask-Login
- CSRF protection
- Protected pages and file download route

## Stack

- Python 3.12+
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- SQLite

## Environment Variables

```env
SECRET_KEY=change-me
DATABASE_URL=sqlite:///users.db
FLASK_DEBUG=true
```

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

- The app auto-creates `users.db` if missing.
- Replace fallback secrets before production.

