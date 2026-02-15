from rest_framework import serializers

from habits.models import Habit
from habits.validators import (PeriodicityValidator, PleasantHabitValidator, RelatedAndAwardValidator,
                               RelatedHabitIsPleasantValidator, TimeExecutionValidator)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов привычек."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)  # Поле user только для чтения
        # ВСЕ валидаторы
        validators = [
            RelatedAndAwardValidator(),
            TimeExecutionValidator(),
            RelatedHabitIsPleasantValidator(),
            PleasantHabitValidator(),
            PeriodicityValidator(),
        ]


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек"""

    class Meta:
        model = Habit
        fields = (
            "id",
            "action",
            "place",
            "time_start",
            "pleasant_habit",
            "related_habit",
            "award",
            "time_execution",
            "is_published",
        )
        read_only_fields = fields  # Все поля только для чтения!
