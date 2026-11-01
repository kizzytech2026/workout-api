
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta


with app.app_context():

    print("Clearing existing data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    squat = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=True
    )

    pushup = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    stretching = Exercise(
        name="Stretching",
        category="Flexibility",
        equipment_needed=False
    )

    db.session.add_all([
        squat,
        pushup,
        running,
        plank,
        stretching
    ])

    db.session.commit()

    print("Creating workouts...")

    workout1 = Workout(
        date=date.today(),
        duration_minutes=60,
        notes="Monday strength training"
    )

    workout2 = Workout(
        date=date.today() - timedelta(days=1),
        duration_minutes=45,
        notes="Cardio and core training"
    )

    workout3 = Workout(
        date=date.today() - timedelta(days=2),
        duration_minutes=30,
        notes="Flexibility and recovery"
    )

    db.session.add_all([workout1, workout2, workout3])

    db.session.commit()

    print("Connecting exercises to workouts...")

    db.session.add_all([
        WorkoutExercise(
            workout=workout1,
            exercise=squat,
            sets=3,
            reps=12
        ),
        WorkoutExercise(
            workout=workout1,
            exercise=pushup,
            sets=3,
            reps=15
        ),
        WorkoutExercise(
            workout=workout1,
            exercise=plank,
            sets=3,
            duration_seconds=60
        ),
        WorkoutExercise(
            workout=workout2,
            exercise=running,
            duration_seconds=1800
        ),
        WorkoutExercise(
            workout=workout2,
            exercise=plank,
            sets=3,
            duration_seconds=45
        ),
        WorkoutExercise(
            workout=workout3,
            exercise=stretching,
            duration_seconds=900
        )
    ])

    db.session.commit()

    print("Database seeded successfully!")
