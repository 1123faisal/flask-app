# Habit Tracker

Flask app for tracking daily habits with MongoDB persistence.

## Features

- Add habits
- Mark habits complete by date
- Browse completion state around selected date
- Server-side rendering with Jinja templates

## Stack

- Python 3.14+
- Flask
- PyMongo
- MongoDB

## Environment Variables

Create `.env`:

```env
MONGODB_URI=mongodb://localhost:27017/habit_tracker
```

## Run Locally

```bash
uv sync
flask --app app run --debug
```

Alternative:

```bash
pip install flask pymongo python-dotenv
flask --app app run --debug
```

Open http://127.0.0.1:5000

