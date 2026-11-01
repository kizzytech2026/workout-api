
from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError
)


CATEGORIES = [
    "Strength",
    "Cardio",
    "Flexibility",
    "Balance",
    "Core"
]


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_training_data(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "Provide either reps or duration_seconds."
            )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.OneOf(CATEGORIES)
    )

    equipment_needed = fields.Bool(required=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=1440)
    )

    notes = fields.Str(
        allow_none=True,
        load_default=None
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates_schema
    def validate_notes(self, data, **kwargs):
        notes = data.get("notes")

        if notes is not None and len(notes) > 2000:
            raise ValidationError(
                {"notes": ["Notes cannot exceed 2000 characters."]}
            )


class WorkoutExerciseInputSchema(Schema):
    reps = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_training_data(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "Provide either reps or duration_seconds."
            )
