from marshmallow import fields, validate

from app.extensions import ma
from app.models import Exercise
from app.models.exercise import VALID_CATEGORIES


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = False
        include_relationships = False

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    category = fields.String(
        required=True, validate=validate.OneOf(sorted(VALID_CATEGORIES))
    )
    equipment_needed = fields.Boolean(required=False)

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True,
        dump_only=True,
    )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
