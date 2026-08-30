from marshmallow import fields, validate

from app.extensions import ma
from app.models import Workout


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = False
        include_relationships = False

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    date = fields.Date(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1)
    )
    notes = fields.String(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True,
        dump_only=True,
    )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
