from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Настройки отображения привычек в админке"""

    list_display = (
        "id",
        "user",
        "place",
        "time_start",
        "action",
        "pleasant_habit",
        "related_habit",
        "periodicity",
        "award",
        "time_execution",
        "is_published",
        "created_at",
    )  # Что показывать в списке
