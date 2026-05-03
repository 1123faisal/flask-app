# Microblog

Flask microblog app backed by MongoDB, with pagination, validation, and health checks.

## Features

- Create short posts
- Paginated home timeline
- Health endpoint for deployment checks
- Basic security response headers
- Environment-based configuration

## Stack

- Python 3.14+
- Flask
- PyMongo
- MongoDB
- Gunicorn (for production)

## Environment Variables

Create `.env`:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=microblog
```

## Run Locally

```bash
uv sync
uv run python main.py
```

Alternative:

```bash
pip install flask pymongo python-dotenv
python main.py
```

Open http://127.0.0.1:5000

## Production Example

```bash
gunicorn "main:app"
```

