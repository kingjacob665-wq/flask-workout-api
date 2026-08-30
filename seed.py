from datetime import date

from app import create_app
from app.extensions import db
from app.models import Workout, Exercise, WorkoutExercise

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    cycling = Exercise(name="Cycling", category="cardio", equipment_needed=True)
    hamstring_stretch = Exercise(
        name="Hamstring Stretch", category="flexibility", equipment_needed=False
    )

    exercises = [push_up, squat, plank, running, cycling, hamstring_stretch]
    db.session.add_all(exercises)
    db.session.commit()

    print("Seeding workouts...")
    morning_strength = Workout(
        name="Morning Strength",
        date=date(2026, 8, 24),
        duration_minutes=45,
        notes="Full body strength session.",
    )
    cardio_blast = Workout(
        name="Cardio Blast",
        date=date(2026, 8, 26),
        duration_minutes=30,
        notes="High-intensity cardio.",
    )
    recovery_day = Workout(
        name="Recovery Day",
        date=date(2026, 8, 28),
        duration_minutes=20,
        notes="Light stretching and mobility work.",
    )

    workouts = [morning_strength, cardio_blast, recovery_day]
    db.session.add_all(workouts)
    db.session.commit()

    print("Linking exercises to workouts...")
    links = [
        WorkoutExercise(
            workout_id=morning_strength.id, exercise_id=push_up.id, sets=3, reps=15
        ),
        WorkoutExercise(
            workout_id=morning_strength.id, exercise_id=squat.id, sets=4, reps=12
        ),
        WorkoutExercise(
            workout_id=morning_strength.id,
            exercise_id=plank.id,
            duration_seconds=60,
        ),
        WorkoutExercise(
            workout_id=cardio_blast.id,
            exercise_id=running.id,
            duration_seconds=1200,
        ),
        WorkoutExercise(
            workout_id=cardio_blast.id, exercise_id=cycling.id, duration_seconds=600
        ),
        WorkoutExercise(
            workout_id=recovery_day.id,
            exercise_id=hamstring_stretch.id,
            sets=2,
            duration_seconds=30,
        ),
    ]
    db.session.add_all(links)
    db.session.commit()

    print("Seeding complete!")
    print(f"Created {len(exercises)} exercises, {len(workouts)} workouts, "
          f"{len(links)} workout-exercise links.")
