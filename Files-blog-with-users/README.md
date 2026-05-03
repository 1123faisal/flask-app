# Files Blog With Users

Full-featured Flask blog app with user accounts, comments, admin-only post management, and contact form email support.

## Features

- User registration and login
- Password hashing with Werkzeug
- Blog post listing and detail pages
- Commenting on posts (authenticated users)
- Admin-only create/edit/delete posts
- Contact form with SMTP integration

## Stack

- Python 3.12+
- Flask
- Flask-Login
- Flask-WTF
- Flask-Bootstrap
- Flask-CKEditor
- Flask-SQLAlchemy
- SQLite

## Environment Variables

Create a `.env` file in this folder:

```env
SECRET_KEY=your-secret-key
MAIL_ADDRESS=your-email@example.com
MAIL_PASSWORD=your-email-password-or-app-password
```

## Run Locally

```bash
uv sync
uv run python main.py
```

Alternative with `requirements.txt`:

```bash
pip install -r requirements.txt
python main.py
```

Open http://127.0.0.1:5000

## Notes

- SQLite database is created automatically as `blog.db`.
- First registered user is typically used as admin in many Flask blog demos.