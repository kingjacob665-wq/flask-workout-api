# Flask Workout Application Backend

## Description

A backend API for a workout tracking application used by personal trainers. The API tracks **Workouts** and reusable **Exercises**, and links them together through an association resource (`WorkoutExercise`) that records the sets, reps, and/or duration for a given exercise within a given workout. This lets a trainer reuse the same exercise across multiple workouts, each time with different sets/reps/duration.

Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow (via Flask-Marshmallow), following REST conventions.

### Data model

- **Workout** — a training session (name, date, duration, notes).
- **Exercise** — a reusable exercise (name, category, whether it needs equipment).
- **WorkoutExercise** — join table/association object connecting a Workout to an Exercise, storing `sets`, `reps`, and `duration_seconds` for that pairing.

A Workout can have many Exercises (through WorkoutExercise), and an Exercise can belong to many Workouts.

## Installation

1. Clone the repo and move into it:
   ```bash
   git clone https://github.com/kingjacob665-wq/flask-workout-api.git
   cd flask-workout-api
   ```

2. Install dependencies with Pipenv:
   ```bash
   pipenv install
   pipenv shell
   ```

3. Set the Flask app environment variable:
   ```bash
   export FLASK_APP=app.py
   ```

4. Run migrations to create the database:
   ```bash
   flask db upgrade
   ```

5. Seed the database with example data:
   ```bash
   python seed.py
   ```

## Running the app

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`.

## Endpoints

### Workouts

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts, including their linked exercises (with sets/reps/duration). |
| GET | `/workouts/<id>` | View a single workout by ID. |
| POST | `/workouts` | Create a new workout. Body: `name` (required), `duration_minutes` (required, positive integer), `date` (optional), `notes` (optional). |
| DELETE | `/workouts/<id>` | Delete a workout (and its exercise links). |
| POST | `/workouts/<id>/exercises` | Add an existing exercise to a workout. Body: `exercise_id` (required), plus optional `sets`, `reps`, `duration_seconds`. |

### Exercises

| Method | Route | Description |
|---|---|---|
| GET | `/exercises` | List all exercises. |
| GET | `/exercises/<id>` | View a single exercise by ID. |
| POST | `/exercises` | Create a new exercise. Body: `name` (required, unique), `category` (required — one of `strength`, `cardio`, `flexibility`, `balance`), `equipment_needed` (optional boolean). |
| DELETE | `/exercises/<id>` | Delete an exercise (and its links to any workouts). |

## Example requests

```bash
# List all workouts (with nested exercises)
curl http://127.0.0.1:5000/workouts

# Create an exercise
curl -X POST http://127.0.0.1:5000/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Deadlift", "category": "strength", "equipment_needed": true}'

# Create a workout
curl -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"name": "Leg Day", "duration_minutes": 40}'

# Add an exercise to a workout
curl -X POST http://127.0.0.1:5000/workouts/1/exercises \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1, "sets": 3, "reps": 8}'

# Delete a workout
curl -X DELETE http://127.0.0.1:5000/workouts/1
```

## Running tests

A small unittest suite covers the main endpoints and validation rules, using an in-memory SQLite database:

```bash
python -m unittest tests.test_api -v
```

## Validations

**Table constraints**
- `workouts.name` and `exercises.name` cannot be empty (`CHECK` constraints).
- `exercises.name` is unique.
- `workouts.duration_minutes` must be positive.
- `workout_exercises.sets` / `reps` / `duration_seconds` must be positive when present.
- `(workout_id, exercise_id)` pairs are unique on `workout_exercises` — an exercise can only be added once per workout.

**Model validations** (SQLAlchemy `@validates`)
- Workout/Exercise names cannot be blank or whitespace-only.
- Exercise `category` must be one of the allowed categories.
- Workout `duration_minutes` and WorkoutExercise `sets`/`reps`/`duration_seconds` must be positive integers when set.

**Schema validations** (Marshmallow)
- Required fields enforced on create (`name`, `duration_minutes`, `category`, `exercise_id`).
- `duration_minutes`, `sets`, `reps`, `duration_seconds` validated with `Range(min=1)`.
- `category` validated with `OneOf` the allowed categories.
- String length limits on names and notes.

## Project structure

```
flask-workout-api/
├── app/
│   ├── __init__.py        # app factory
│   ├── extensions.py       # db, migrate, ma instances
│   ├── models/              # Workout, Exercise, WorkoutExercise
│   ├── schemas/             # Marshmallow schemas
│   └── routes/               # Blueprints
├── migrations/              # Flask-Migrate migrations
├── tests/                    # unittest suite
│   └── test_api.py
├── app.py                   # entry point
├── seed.py                  # seed script
├── config.py
├── Pipfile
└── README.md
```
