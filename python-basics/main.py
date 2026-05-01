import datetime
import os
from typing import Any

from flask import Flask, redirect, render_template, request, url_for
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError

MAX_POST_LENGTH = 500


def create_app() -> Flask:
    app = Flask(__name__)
    mongodb_uri = (
        os.getenv("MONGODB_URI")
        or os.getenv("MONGO_URI")
        or "mongodb://localhost:27017"
    )
    mongodb_db_name = os.getenv("MONGODB_DB_NAME", "microblog")

    db: Any = None
    db_error = None

    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[mongodb_db_name]
    except PyMongoError:
        db_error = (
            "Database connection failed. Set MONGODB_URI (or MONGO_URI) to your "
            "MongoDB connection string, or run local MongoDB."
        )

    def create_entry(content: str) -> None:
        if db is None:
            raise RuntimeError("Database is not connected.")

        # Store full UTC timestamp — clients format it in their own timezone.
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        db.entries.insert_one(
            {
                "content": content,
                "timestamp": now_utc.isoformat(),
            }
        )

    def fetch_entries(limit: int = 100) -> list[dict]:
        if db is None:
            return []

        # Keep feed lightweight and newest-first.
        cursor = db.entries.find({}, {"_id": 0}).sort("_id", DESCENDING).limit(limit)
        return list(cursor)

    @app.route("/", methods=["GET", "POST"])
    def home():
        error = db_error

        if request.method == "POST":
            entry_content = (request.form.get("content") or "").strip()

            if not entry_content:
                error = "Entry cannot be empty."
            elif len(entry_content) > MAX_POST_LENGTH:
                error = f"Entry cannot exceed {MAX_POST_LENGTH} characters."
            else:
                try:
                    create_entry(entry_content)
                    return redirect(url_for("home"))
                except (PyMongoError, RuntimeError):
                    error = "Could not save entry right now. Please try again."

        try:
            entries = fetch_entries()
        except PyMongoError:
            entries = []
            if error is None:
                error = "Could not load entries right now."

        return render_template(
            "home.html", entries=entries, name="My Microblog", error=error
        )

    return app


app = create_app()
