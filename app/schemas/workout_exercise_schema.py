from marshmallow import fields, validate

from app.extensions import ma
from app.models import WorkoutExercise


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = False
        include_fk = True

    id = fields.Integer(dump_only=True)
    sets = fields.Integer(
        required=False, allow_none=True, validate=validate.Range(min=1)
    )
    reps = fields.Integer(
        required=False, allow_none=True, validate=validate.Range(min=1)
    )
    duration_seconds = fields.Integer(
        required=False, allow_none=True, validate=validate.Range(min=1)
    )

    exercise = fields.Nested(
        "ExerciseSchema", exclude=("workout_exercises",), dump_only=True
    )


workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
