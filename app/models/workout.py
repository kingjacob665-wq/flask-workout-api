from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from app.extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_workout_name_not_empty"),
        CheckConstraint(
            "duration_minutes > 0", name="ck_workout_duration_positive"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Association object relationship: Workout <-> Exercise through WorkoutExercise
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True,
        back_populates="workouts",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        return value.strip()

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration_minutes must be a positive integer.")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.name}>"
