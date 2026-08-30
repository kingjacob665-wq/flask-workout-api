from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Exercise
from app.schemas import exercise_schema, exercises_schema

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("")
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercises_bp.get("/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@exercises_bp.post("")
def create_exercise():
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"error": "No input data provided."}), 400

    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    try:
        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data.get("equipment_needed", False),
        )
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 422

    return jsonify(exercise_schema.dump(exercise)), 201


@exercises_bp.delete("/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {exercise_id} deleted."}), 200
