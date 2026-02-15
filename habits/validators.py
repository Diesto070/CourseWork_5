from rest_framework import serializers


class RelatedAndAwardValidator:
    """
    Проверяет, что не заполнены одновременно related_habit и award.
    Можно заполнить только одно из двух полей.
    """

    def __call__(self, data):
        if data.get("related_habit") and data.get("award"):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать и связанную привычку, и вознаграждение. " "Выберите что-то одно."
            )
        return data


class TimeExecutionValidator:
    """Проверяет время выполнения (не более 120 секунд)."""

    def __call__(self, data):
        time_execution = data.get("time_execution")
        if time_execution and time_execution > 120:
            raise serializers.ValidationError({"time_execution": "Время выполнения не должно превышать 120 секунд."})
        return data


class RelatedHabitIsPleasantValidator:
    """Проверяет, что связанная привычка является приятной."""

    def __call__(self, data):
        related_habit = data.get("related_habit")
        if related_habit and not related_habit.pleasant_habit:
            raise serializers.ValidationError({"related_habit": "Связанная привычка должна быть приятной."})
        return data


class PleasantHabitValidator:
    """Проверяет правила для приятных привычек."""

    def __call__(self, data):
        pleasant_habit = data.get("pleasant_habit", False)

        if pleasant_habit:
            if data.get("related_habit"):
                raise serializers.ValidationError(
                    {"related_habit": "У приятной привычки не может быть связанной привычки."}
                )
            if data.get("award"):
                raise serializers.ValidationError({"award": "У приятной привычки не может быть вознаграждения."})
        return data


class PeriodicityValidator:
    """Проверяет периодичность (1-7 дней)."""

    def __call__(self, data):
        periodicity = data.get("periodicity")
        if periodicity:
            if periodicity < 1:
                raise serializers.ValidationError({"periodicity": "Периодичность не может быть меньше 1 дня."})
            if periodicity > 7:
                raise serializers.ValidationError({"periodicity": "Периодичность не может быть больше 7 дней."})
        return data
