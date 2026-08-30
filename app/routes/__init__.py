from app.routes.workouts import workouts_bp
from app.routes.exercises import exercises_bp


def register_routes(app):
    app.register_blueprint(workouts_bp)
    app.register_blueprint(exercises_bp)
