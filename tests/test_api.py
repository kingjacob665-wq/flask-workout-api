import unittest

from app import create_app
from app.extensions import db
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


class WorkoutApiTestCase(unittest.TestCase):
    """Basic coverage for the Workout API's endpoints and validations."""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---- Exercises ----

    def test_create_exercise_success(self):
        resp = self.client.post(
            "/exercises",
            json={"name": "Push Up", "category": "strength"},
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["name"], "Push Up")

    def test_create_exercise_invalid_category_rejected(self):
        resp = self.client.post(
            "/exercises",
            json={"name": "Push Up", "category": "not-real"},
        )
        self.assertEqual(resp.status_code, 422)

    def test_create_exercise_duplicate_name_rejected(self):
        self.client.post(
            "/exercises", json={"name": "Push Up", "category": "strength"}
        )
        resp = self.client.post(
            "/exercises", json={"name": "Push Up", "category": "strength"}
        )
        self.assertEqual(resp.status_code, 422)

    def test_get_exercises_list(self):
        self.client.post(
            "/exercises", json={"name": "Squat", "category": "strength"}
        )
        resp = self.client.get("/exercises")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

    def test_delete_exercise(self):
        create = self.client.post(
            "/exercises", json={"name": "Plank", "category": "strength"}
        )
        exercise_id = create.get_json()["id"]
        resp = self.client.delete(f"/exercises/{exercise_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.get(f"/exercises/{exercise_id}").status_code, 404)

    # ---- Workouts ----

    def test_create_workout_success(self):
        resp = self.client.post(
            "/workouts", json={"name": "Leg Day", "duration_minutes": 40}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["name"], "Leg Day")

    def test_create_workout_negative_duration_rejected(self):
        resp = self.client.post(
            "/workouts", json={"name": "Leg Day", "duration_minutes": -5}
        )
        self.assertEqual(resp.status_code, 422)

    def test_get_single_workout_not_found(self):
        resp = self.client.get("/workouts/999")
        self.assertEqual(resp.status_code, 404)

    def test_delete_workout(self):
        create = self.client.post(
            "/workouts", json={"name": "Recovery", "duration_minutes": 20}
        )
        workout_id = create.get_json()["id"]
        resp = self.client.delete(f"/workouts/{workout_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.get(f"/workouts/{workout_id}").status_code, 404)

    # ---- Adding exercises to workouts ----

    def test_add_exercise_to_workout(self):
        workout = self.client.post(
            "/workouts", json={"name": "Leg Day", "duration_minutes": 40}
        ).get_json()
        exercise = self.client.post(
            "/exercises", json={"name": "Squat", "category": "strength"}
        ).get_json()

        resp = self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json={"exercise_id": exercise["id"], "sets": 3, "reps": 10},
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(resp.get_json()["workout_exercises"]), 1)

    def test_add_same_exercise_twice_rejected(self):
        workout = self.client.post(
            "/workouts", json={"name": "Leg Day", "duration_minutes": 40}
        ).get_json()
        exercise = self.client.post(
            "/exercises", json={"name": "Squat", "category": "strength"}
        ).get_json()

        self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json={"exercise_id": exercise["id"], "sets": 3, "reps": 10},
        )
        resp = self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json={"exercise_id": exercise["id"], "sets": 3, "reps": 10},
        )
        self.assertEqual(resp.status_code, 422)

    def test_add_exercise_invalid_reps_rejected(self):
        workout = self.client.post(
            "/workouts", json={"name": "Leg Day", "duration_minutes": 40}
        ).get_json()
        exercise = self.client.post(
            "/exercises", json={"name": "Squat", "category": "strength"}
        ).get_json()

        resp = self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json={"exercise_id": exercise["id"], "reps": 0},
        )
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
