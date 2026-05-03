from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

from routes import pages

load_dotenv()


def create_app():
    app = Flask(__name__)

    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        database: Database = client.get_default_database()
        app.extensions["db"] = database
        print("Database Connected.", database.name)
    except PyMongoError as exc:
        print("Database Error.", exc)

    app.register_blueprint(pages)

    return app
