from django.db import models

from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """Модель привычки."""

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # ⬅ ВРЕМЕННО: делаем необязательным
        blank=True,  # ⬅ ВРЕМЕННО
        related_name="habits",
        verbose_name="Пользователь",
        help_text="Укажите создателя привычки",
    )
    place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место",
        help_text="Укажите место выполнения привычки",
    )
    time_start = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Время начала",
        help_text="Укажите время начала выполнения привычки",
    )
    action = models.CharField(
        max_length=200,
        verbose_name="Действие",
        help_text="Укажите действие",
    )
    pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Укажите, является ли привычка приятной",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
    )
    periodicity = models.IntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки",
    )
    award = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение за выполнение привычки",
    )
    time_execution = models.IntegerField(
        default=120,
        blank=True,
        null=True,
        verbose_name="Время выполнения",
        help_text="Укажите время выполнения привычки (в секундах)",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Публичность",
        help_text="Признак публичности",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.action} в {self.time_start}"
