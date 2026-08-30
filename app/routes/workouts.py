from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Workout, Exercise, WorkoutExercise
from app.schemas import (
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.get("")
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workouts_bp.get("/<int:workout_id>")
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found."}), 404
    return jsonify(workout_schema.dump(workout)), 200


@workouts_bp.post("")
def create_workout():
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"error": "No input data provided."}), 400

    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    try:
        workout = Workout(
            name=data["name"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes"),
        )
        if data.get("date"):
            workout.date = data["date"]
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 422

    return jsonify(workout_schema.dump(workout)), 201


@workouts_bp.delete("/<int:workout_id>")
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {workout_id} deleted."}), 200


@workouts_bp.post("/<int:workout_id>/exercises")
def add_exercise_to_workout(workout_id):
    """Add an existing exercise to a workout, with sets/reps/duration."""
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    json_data = request.get_json(silent=True)
    if not json_data or "exercise_id" not in json_data:
        return jsonify({"error": "exercise_id is required."}), 400

    exercise = Exercise.query.get(json_data["exercise_id"])
    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    payload = {
        "workout_id": workout.id,
        "exercise_id": exercise.id,
        "sets": json_data.get("sets"),
        "reps": json_data.get("reps"),
        "duration_seconds": json_data.get("duration_seconds"),
    }

    try:
        validated = workout_exercise_schema.load(payload)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    try:
        link = WorkoutExercise(
            workout_id=validated["workout_id"],
            exercise_id=validated["exercise_id"],
            sets=validated.get("sets"),
            reps=validated.get("reps"),
            duration_seconds=validated.get("duration_seconds"),
        )
        db.session.add(link)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 422

    return jsonify(workout_schema.dump(workout)), 201
