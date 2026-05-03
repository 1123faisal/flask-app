# Python Demo Workspace

This repository is a collection of small Flask, Python, and JavaScript projects built for learning and portfolio practice.

## Projects

| Project | Type | README |
|---|---|---|
| cafe-api | Flask REST API + SQLite | [cafe-api/README.md](cafe-api/README.md) |
| Files-blog-with-users | Flask blog with authentication | [Files-blog-with-users/README.md](Files-blog-with-users/README.md) |
| flask-auth-start | Flask auth starter app | [flask-auth-start/README.md](flask-auth-start/README.md) |
| flask-portfolio | Flask portfolio website | [flask-portfolio/README.md](flask-portfolio/README.md) |
| habit-tracker | Flask + MongoDB habit tracker | [habit-tracker/README.md](habit-tracker/README.md) |
| lib-crud | Flask CRUD app for books | [lib-crud/README.md](lib-crud/README.md) |
| microblog | Flask + MongoDB microblog | [microblog/README.md](microblog/README.md) |
| project-quote-generator | Node.js DOCX quote generator | [project-quote-generator/README.md](project-quote-generator/README.md) |
| tindog | Flask multi-page demo app | [tindog/README.md](tindog/README.md) |
| tindog/oop | Python OOP coffee machine exercise | [tindog/oop/README.md](tindog/oop/README.md) |
| top-10-movies | Flask movie ranking app | [top-10-movies/README.md](top-10-movies/README.md) |

## Workspace Prerequisites

- Python 3.12+ (some projects specify 3.14 in `pyproject.toml`)
- Node.js 18+ (for `project-quote-generator`)
- `uv` (recommended) or `pip`
- MongoDB running locally or a MongoDB Atlas URI (for MongoDB projects)

## Quick Start Pattern

Use these commands inside each project folder:

```bash
# if the project has pyproject.toml
uv sync
uv run python <entry-file>.py

# or with pip
pip install -r requirements.txt
python <entry-file>.py
```

For factory-style Flask apps, use:

```bash
flask --app app run --debug
```

## Notes

- Most projects use SQLite databases created automatically in an `instance` folder.
- Never commit real API keys, secret keys, or email credentials.
- Several demo apps use hard-coded development defaults. Replace these before deployment.
