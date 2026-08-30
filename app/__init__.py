from flask import Flask, jsonify

from config import Config
from app.extensions import db, migrate, ma


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        from app import models  # noqa: F401 - register models with SQLAlchemy

        from app.routes import register_routes

        register_routes(app)

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "Workout Application Backend API",
                "endpoints": [
                    "GET /workouts",
                    "GET /workouts/<id>",
                    "POST /workouts",
                    "DELETE /workouts/<id>",
                    "POST /workouts/<id>/exercises",
                    "GET /exercises",
                    "GET /exercises/<id>",
                    "POST /exercises",
                    "DELETE /exercises/<id>",
                ],
            }
        )

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request."}), 400

    return app
