# my_project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
from flasgger import Swagger

load_dotenv()

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# Глобальний інстанс БД, який імпортують інші модулі як: from my_project import db
db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=SECRET_KEY,
        SWAGGER={'title': 'My Project API', 'uiversion': 3},
    )

    Swagger(app)
    _init_db(app)

    # ВАЖЛИВО: імпортуємо маршрути лише після ініціалізації app/db
    from my_project.auth.route import register_routes
    register_routes(app)

    return app

def _init_db(app: Flask) -> None:
    db.init_app(app)
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        import my_project.auth.domain  # моделі
        db.create_all()
