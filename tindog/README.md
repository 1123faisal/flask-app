# TinDog Flask App

Multi-page Flask demo application combining a CV page, blog pages, TinDog landing page, login flow, and an API-powered gender guess feature.

## Routes

- `/` CV/home page
- `/blogs` blog listing from remote JSON
- `/blogs/<id>` blog details
- `/tindog` marketing landing page
- `/login` demo login
- `/logout` clear session
- `/guess/<name>` gender prediction via Genderize API

## Stack

- Python 3.12+
- Flask
- Requests
- Jinja templates
- Bootstrap-based UI

## Run Locally

```bash
uv sync
uv run python server.py
```

Alternative:

```bash
pip install flask requests
python server.py
```

Open http://127.0.0.1:5000

## Demo Login

- Email: `demo@tindog.com`
- Password: `password123`

## Notes

- Replace demo credentials before production use.
- Blog data comes from a remote npoint endpoint.

