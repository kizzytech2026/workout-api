# Workout Tracking API

## Overview

The Workout Tracking API is a RESTful API built with Python, Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

The application helps personal trainers manage workouts and exercises. It allows users to create, retrieve, and delete workouts and exercises, as well as associate exercises with specific workouts.

## Technologies Used

- Python 3.8.13
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- SQLAlchemy
- Marshmallow 3.20.1
- SQLite
- Pytest

## Project Structure

```text
workout-api/
│
├── Pipfile
├── Pipfile.lock
├── README.md
├── .gitignore
│
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    ├── test_app.py
    ├── migrations/
    └── instance/
        └── app.db
```

## Database Models

### 1. Exercise

Stores information about exercises.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Exercise name |
| category | String | Exercise category |
| equipment_needed | Boolean | Whether equipment is required |

Supported categories:

- Strength
- Cardio
- Flexibility
- Balance
- Core

### 2. Workout

Stores information about individual workouts.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| date | Date | Workout date |
| duration_minutes | Integer | Workout duration |
| notes | Text | Additional workout notes |

### 3. WorkoutExercise

Connects workouts and exercises through a many-to-many relationship.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| workout_id | Integer | Foreign key referencing Workout |
| exercise_id | Integer | Foreign key referencing Exercise |
| reps | Integer | Number of repetitions |
| sets | Integer | Number of sets |
| duration_seconds | Integer | Exercise duration |

## Relationships

- One workout can contain multiple exercises.
- One exercise can belong to multiple workouts.
- WorkoutExercise connects Workout and Exercise.
- WorkoutExercise stores exercise-specific information such as reps, sets, and duration.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd workout-api
```

### 2. Install dependencies

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

### 3. Navigate to the server directory

```bash
cd server
```

### 4. Configure Flask

```bash
export FLASK_APP=app.py
```

### 5. Initialize database migrations

Only run this command if the migrations directory does not already exist:

```bash
python -m flask db init
```

Generate and apply migrations:

```bash
python -m flask db migrate -m "Create workout exercise and workout tables"
python -m flask db upgrade
```

### 6. Seed the database

```bash
python seed.py
```

### 7. Run the application

```bash
python app.py
```

The application runs at:

http://127.0.0.1:5555

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example API Requests

### Create an Exercise

**POST** `/exercises`

```json
{
    "name": "Squats",
    "category": "Strength",
    "equipment_needed": true
}
```

### Create a Workout

**POST** `/workouts`

```json
{
    "date": "2026-10-31",
    "duration_minutes": 60,
    "notes": "Full body strength training"
}
```

### Add an Exercise to a Workout

**POST** `/workouts/1/exercises/1/workout_exercises`

```json
{
    "reps": 12,
    "sets": 3
}
```

### Add a Timed Exercise

**POST** `/workouts/1/exercises/2/workout_exercises`

```json
{
    "duration_seconds": 60
}
```

## Validation and Error Handling

The application uses three levels of validation:

1. **Database-level validation:** SQLAlchemy constraints protect database integrity, including positive workout duration, positive exercise values, and unique workout-exercise combinations.
2. **Model-level validation:** SQLAlchemy validators check exercise names, categories, workout duration, repetitions, sets, and exercise duration.
3. **Schema-level validation:** Marshmallow validates incoming JSON data, required fields, data types, and allowed values.

The API also returns appropriate HTTP status codes:

- `200` – Successful request.
- `201` – Resource successfully created.
- `400` – Invalid input or database constraint violation.
- `404` – Requested resource not found.

## Running Tests

The project uses Pytest.

Install Pytest:

```bash
python -m pip install pytest
```

Run the tests from the server directory:

```bash
python -m pytest -v
```

The test suite covers:

- Home route.
- Creating and retrieving workouts.
- Creating and retrieving exercises.
- Deleting workouts and exercises.
- Invalid input validation.
- Adding exercises to workouts.
- Duplicate exercise associations.
- Missing resource handling.

## Database

The application uses SQLite for data storage.

Database migrations are managed using Flask-Migrate and Alembic.

## Author

Developed as a Workout Tracking API project using Python and Flask.

