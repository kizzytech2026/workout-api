
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseInputSchema
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# Initialize schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_input_schema = WorkoutExerciseInputSchema()


# Helper function for errors
def error_response(message, status_code):
    return make_response(jsonify({"error": message}), status_code)


# HOME ROUTE
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Workout Tracking API",
        "endpoints": [
            "/workouts",
            "/exercises"
        ]
    }), 200


# =====================================
# WORKOUT ROUTES
# =====================================

# GET all workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()

    return jsonify(workouts_schema.dump(workouts)), 200


# GET one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return error_response("Workout not found.", 404)

    return jsonify(workout_schema.dump(workout)), 200


# CREATE workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True) or {}

    try:
        validated_data = workout_schema.load(data)

        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as err:
        db.session.rollback()
        return jsonify({"errors": err.messages}), 400

    except ValueError as err:
        db.session.rollback()
        return error_response(str(err), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response("Database constraint violation.", 400)


# DELETE workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return error_response("Workout not found.", 404)

    try:
        db.session.delete(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout deleted successfully."
        }), 200

    except IntegrityError:
        db.session.rollback()
        return error_response("Could not delete workout.", 400)


# =====================================
# EXERCISE ROUTES
# =====================================

# GET all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()

    return jsonify(exercises_schema.dump(exercises)), 200


# GET one exercise
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return error_response("Exercise not found.", 404)

    return jsonify(exercise_schema.dump(exercise)), 200


# CREATE exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True) or {}

    try:
        validated_data = exercise_schema.load(data)

        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as err:
        db.session.rollback()
        return jsonify({"errors": err.messages}), 400

    except ValueError as err:
        db.session.rollback()
        return error_response(str(err), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response("Database constraint violation.", 400)


# DELETE exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return error_response("Exercise not found.", 404)

    try:
        db.session.delete(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully."
        }), 200

    except IntegrityError:
        db.session.rollback()
        return error_response("Could not delete exercise.", 400)


# =====================================
# WORKOUT EXERCISE ROUTE
# =====================================

# ADD exercise to workout
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return error_response("Workout not found.", 404)

    if not exercise:
        return error_response("Exercise not found.", 404)

    data = request.get_json(silent=True) or {}

    try:
        validated_data = workout_exercise_input_schema.load(data)

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated_data
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise added to workout successfully.",
            "workout_exercise": {
                "id": workout_exercise.id,
                "workout_id": workout_exercise.workout_id,
                "exercise_id": workout_exercise.exercise_id,
                "exercise_name": exercise.name,
                "reps": workout_exercise.reps,
                "sets": workout_exercise.sets,
                "duration_seconds": workout_exercise.duration_seconds
            }
        }), 201

    except ValidationError as err:
        db.session.rollback()
        return jsonify({"errors": err.messages}), 400

    except ValueError as err:
        db.session.rollback()
        return error_response(str(err), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "This exercise may already exist in this workout, "
            "or the data violates a database constraint.",
            400
        )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
