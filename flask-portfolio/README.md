# Flask Portfolio

Portfolio-style Flask web app with project cards, detail pages, auth flow, and custom error pages.

## Features

- Portfolio homepage with project listing
- Detail pages by slug
- Sign up and login flow (in-memory user store)
- Protected page example
- Custom 401, 404, and 500 templates

## Stack

- Python 3.14+
- Flask
- Jinja templates
- HTML/CSS

## Run Locally

From this folder:

```bash
uv sync
flask --app portfolio run --debug
```

Alternative:

```bash
pip install flask
flask --app portfolio run --debug
```

Open http://127.0.0.1:5000

## Notes

- User accounts are stored in memory and reset when the app restarts.
- `portfolio/__init__.py` contains routes and app creation.
