# Cafe API

Flask REST API for managing a cafe directory stored in SQLite.

## Features

- List all cafes
- Fetch a random cafe
- Search cafes by location
- Add new cafes
- Update coffee price
- Delete cafes with API key protection

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
pip install flask flask-sqlalchemy
python main.py
```

Open http://127.0.0.1:5000

## API Endpoints

- `GET /all`
- `GET /random`
- `GET /search?loc=<location>`
- `POST /add`
- `PATCH /update-price/<cafe_id>?new_price=<value>`
- `DELETE /report-closed/<cafe_id>?api-key=TopSecretAPIKey`

## Notes

- Database file is created automatically.
- `cafe-api.http` contains sample HTTP requests.
