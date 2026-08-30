from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from app.extensions import db

VALID_CATEGORIES = {"strength", "cardio", "flexibility", "balance"}


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        db.UniqueConstraint("name", name="uq_exercise_name"),
        CheckConstraint("length(name) > 0", name="ck_exercise_name_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True,
        back_populates="exercises",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or value.lower() not in VALID_CATEGORIES:
            raise ValueError(
                f"Exercise category must be one of {sorted(VALID_CATEGORIES)}."
            )
        return value.lower()

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"
