import datetime
import logging
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from flask import Flask, Response, redirect, render_template, request, url_for
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_POST_LENGTH = 500
PAGE_SIZE = 20


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    mongodb_uri: str
    db_name: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            mongodb_uri=(
                os.getenv("MONGODB_URI")
                or os.getenv("MONGO_URI")
                or "mongodb://localhost:27017"
            ),
            db_name=os.getenv("MONGODB_DB_NAME", "microblog"),
        )


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def connect_db(config: Config) -> tuple[Any, str | None]:
    """Return (db, error_message). error_message is None on success."""
    try:
        client = MongoClient(
            config.mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            maxPoolSize=50,       # handles concurrent gunicorn workers cleanly
            retryWrites=True,
        )
        client.admin.command("ping")
        db = client[config.db_name]
        # Ascending index on timestamp keeps sort + pagination fast at scale.
        db.entries.create_index([("timestamp", ASCENDING)], background=True)
        # Mask credentials in log output.
        safe_uri = config.mongodb_uri.split("@")[-1]
        logger.info("MongoDB connected: %s / %s", safe_uri, config.db_name)
        return db, None
    except PyMongoError as exc:
        logger.error("MongoDB connection failed: %s", exc)
        return None, "Database connection failed. Check your MONGODB_URI setting."


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app(config: Config | None = None) -> Flask:
    cfg = config or Config.from_env()
    app = Flask(__name__)

    db, db_error = connect_db(cfg)

    # -- Security headers ----------------------------------------------------

    @app.after_request
    def set_security_headers(response: Response) -> Response:
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy", "strict-origin-when-cross-origin"
        )
        return response

    # -- Error handlers ------------------------------------------------------

    @app.errorhandler(404)
    def not_found(_exc: Exception) -> tuple[str, int]:
        return (
            render_template(
                "home.html",
                entries=[],
                name="My Microblog",
                error="Page not found.",
                page=1,
                has_more=False,
            ),
            404,
        )

    @app.errorhandler(500)
    def server_error(_exc: Exception) -> tuple[str, int]:
        logger.exception("Unhandled server error")
        return (
            render_template(
                "home.html",
                entries=[],
                name="My Microblog",
                error="Something went wrong. Please try again.",
                page=1,
                has_more=False,
            ),
            500,
        )

    # -- DB helpers ----------------------------------------------------------

    def create_entry(content: str) -> None:
        if db is None:
            raise RuntimeError("Database is not connected.")
        db.entries.insert_one(
            {
                "content": content,
                # Native datetime so MongoDB can index/sort efficiently.
                "timestamp": datetime.datetime.now(datetime.timezone.utc),
            }
        )

    def fetch_entries(page: int = 1) -> tuple[list[dict], bool]:
        """Return (entries_for_page, has_more)."""
        if db is None:
            return [], False
        skip = (page - 1) * PAGE_SIZE
        rows = list(
            db.entries.find({}, {"_id": 0})
            .sort("timestamp", DESCENDING)
            .skip(skip)
            .limit(PAGE_SIZE + 1)   # fetch one extra to detect next page
        )
        has_more = len(rows) > PAGE_SIZE
        # Convert native datetime → ISO string for template/JS consumption.
        for row in rows[:PAGE_SIZE]:
            if isinstance(row.get("timestamp"), datetime.datetime):
                row["timestamp"] = row["timestamp"].isoformat()
        return rows[:PAGE_SIZE], has_more

    # -- Routes --------------------------------------------------------------

    @app.get("/health")
    def health() -> tuple[dict, int]:
        """Liveness probe for Render / load balancers."""
        if db is None:
            return {"status": "degraded", "db": False}, 503
        return {"status": "ok", "db": True}, 200

    @app.route("/", methods=["GET", "POST"])
    def home():
        error = db_error
        page = max(1, request.args.get("page", 1, type=int))

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
                except (PyMongoError, RuntimeError) as exc:
                    logger.error("Entry insert failed: %s", exc)
                    error = "Could not save entry right now. Please try again."

        try:
            entries, has_more = fetch_entries(page=page)
        except PyMongoError as exc:
            logger.error("Entry fetch failed: %s", exc)
            entries, has_more = [], False
            if error is None:
                error = "Could not load entries right now."

        return render_template(
            "home.html",
            entries=entries,
            name="My Microblog",
            error=error,
            page=page,
            has_more=has_more,
        )

    return app


app = create_app()
