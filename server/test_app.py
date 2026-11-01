
import pytest

from app import app
from models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture
def client():
    """Create a fresh test database for every test."""

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.drop_all()
        db.create_all()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Welcome to the Workout Tracking API"


# --------------------------------------------------
# EXERCISE TESTS
# --------------------------------------------------

def test_get_exercises(client):
    response = client.get("/exercises")

    assert response.status_code == 200
    assert response.json == []


def test_create_exercise(client):
    response = client.post("/exercises", json={
        "name": "Squats",
        "category": "Strength",
        "equipment_needed": True
    })

    assert response.status_code == 201
    assert response.json["name"] == "Squats"
    assert response.json["category"] == "Strength"
    assert response.json["equipment_needed"] is True


def test_create_exercise_with_invalid_name(client):
    response = client.post("/exercises", json={
        "name": "A",
        "category": "Strength",
        "equipment_needed": True
    })

    assert response.status_code == 400


def test_create_exercise_with_invalid_category(client):
    response = client.post("/exercises", json={
        "name": "Squats",
        "category": "Invalid",
        "equipment_needed": True
    })

    assert response.status_code == 400


def test_get_single_exercise(client):
    exercise = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.get("/exercises/1")

    assert response.status_code == 200
    assert response.json["name"] == "Push-ups"


def test_get_nonexistent_exercise(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404


def test_delete_exercise(client):
    exercise = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.delete("/exercises/1")

    assert response.status_code == 200
    assert response.json["message"] == "Exercise deleted successfully."


def test_delete_nonexistent_exercise(client):
    response = client.delete("/exercises/999")

    assert response.status_code == 404


# --------------------------------------------------
# WORKOUT TESTS
# --------------------------------------------------

def test_get_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert response.json == []


def test_create_workout(client):
    response = client.post("/workouts", json={
        "date": "2026-10-31",
        "duration_minutes": 60,
        "notes": "Strength training"
    })

    assert response.status_code == 201
    assert response.json["duration_minutes"] == 60
    assert response.json["notes"] == "Strength training"


def test_create_workout_with_invalid_duration(client):
    response = client.post("/workouts", json={
        "date": "2026-10-31",
        "duration_minutes": -10,
        "notes": "Invalid workout"
    })

    assert response.status_code == 400


def test_get_single_workout(client):
    from datetime import date

    workout = Workout(
        date=date(2026, 10, 31),
        duration_minutes=45,
        notes="Morning workout"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.get("/workouts/1")

    assert response.status_code == 200
    assert response.json["duration_minutes"] == 45


def test_get_nonexistent_workout(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404


def test_delete_workout(client):
    from datetime import date

    workout = Workout(
        date=date(2026, 10, 31),
        duration_minutes=30,
        notes="Evening workout"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.delete("/workouts/1")

    assert response.status_code == 200
    assert response.json["message"] == "Workout deleted successfully."


def test_delete_nonexistent_workout(client):
    response = client.delete("/workouts/999")

    assert response.status_code == 404


# --------------------------------------------------
# WORKOUT-EXERCISE ASSOCIATION TESTS
# --------------------------------------------------

@pytest.fixture
def sample_workout_and_exercise(client):
    """Create one workout and one exercise for association tests."""

    from datetime import date

    workout = Workout(
        date=date(2026, 10, 31),
        duration_minutes=60,
        notes="Full body workout"
    )

    exercise = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=True
    )

    db.session.add_all([workout, exercise])
    db.session.commit()

    return workout.id, exercise.id


def test_add_exercise_to_workout(client, sample_workout_and_exercise):
    workout_id, exercise_id = sample_workout_and_exercise

    response = client.post(
        "/workouts/{}/exercises/{}/workout_exercises".format(
            workout_id, exercise_id
        ),
        json={
            "reps": 12,
            "sets": 3
        }
    )

    assert response.status_code == 201
    assert response.json["workout_exercise"]["reps"] == 12
    assert response.json["workout_exercise"]["sets"] == 3
    assert response.json["workout_exercise"]["exercise_name"] == "Squats"


def test_add_exercise_with_duration(client, sample_workout_and_exercise):
    workout_id, exercise_id = sample_workout_and_exercise

    response = client.post(
        "/workouts/{}/exercises/{}/workout_exercises".format(
            workout_id, exercise_id
        ),
        json={
            "duration_seconds": 60
        }
    )

    assert response.status_code == 201
    assert response.json["workout_exercise"]["duration_seconds"] == 60


def test_add_exercise_without_training_data(
    client, sample_workout_and_exercise
):
    workout_id, exercise_id = sample_workout_and_exercise

    response = client.post(
        "/workouts/{}/exercises/{}/workout_exercises".format(
            workout_id, exercise_id
        ),
        json={}
    )

    assert response.status_code == 400


def test_add_exercise_to_nonexistent_workout(client):
    exercise = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.post(
        "/workouts/999/exercises/1/workout_exercises",
        json={"reps": 10}
    )

    assert response.status_code == 404


def test_add_nonexistent_exercise_to_workout(client):
    from datetime import date

    workout = Workout(
        date=date(2026, 10, 31),
        duration_minutes=30,
        notes="Test workout"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.post(
        "/workouts/1/exercises/999/workout_exercises",
        json={"reps": 10}
    )

    assert response.status_code == 404


def test_duplicate_exercise_in_workout(
    client, sample_workout_and_exercise
):
    workout_id, exercise_id = sample_workout_and_exercise

    url = "/workouts/{}/exercises/{}/workout_exercises".format(
        workout_id, exercise_id
    )

    first_response = client.post(url, json={"reps": 10})
    second_response = client.post(url, json={"reps": 15})

    assert first_response.status_code == 201
    assert second_response.status_code == 400
