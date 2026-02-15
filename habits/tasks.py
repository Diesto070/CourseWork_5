from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def check_all_habits_and_send_reminders():
    """Проверка всех привычек и отправка напоминаний."""
    # Получаем текущее время
    now = timezone.localtime()  # Получаем текущее время с учетом часового пояса
    current_time = now.time()  # Извлекаем только время из даты-времени
    today = now.date()  # Получение СЕГОДНЯШНЕЙ ДАТЫ

    # Находим все привычки с указанным временем и привязанным Telegram
    habits = Habit.objects.filter(time_start__isnull=False, user__tg_id__isnull=False)

    # Проверяем каждую привычку
    for habit in habits:
        habit_time = habit.time_start

        # Пропускаем приятные привычки (им не нужны напоминания)
        if habit_time and not habit.pleasant_habit:

            # Проверяем, совпадает ли текущее время с временем привычки (с допуском ±2 минуты)
            time_diff = abs(
                (current_time.hour * 60 + current_time.minute) - (habit_time.hour * 60 + habit_time.minute)
            )

            # Если время совпадает - отправляем напоминание
            if time_diff <= 2:
                # Ключ для хранения даты последней отправки
                last_sent_key = f"last_sent_{habit.id}"

                # Получаем дату последней отправки из кэша
                last_sent_date = cache.get(last_sent_key)

                # Проверяем нужно ли отправлять
                need_to_send = False

                if not last_sent_date:
                    need_to_send = True  # Первый раз
                else:
                    # Считаем разницу в днях
                    days_diff = (today - last_sent_date).days
                    if days_diff >= habit.periodicity:
                        need_to_send = True

                # Отправляем напоминание в Telegram
                if need_to_send:
                    # Формируем сообщение
                    message = (
                        f"Напоминание!\n\n "
                        f"Я буду {habit.action} в {habit_time.strftime('%H:%M')} "
                        f"в {habit.place if habit.place else 'удобном месте'}"
                    )
                    if send_telegram_message(habit.user.tg_id, message):
                        # Сохраняем дату отправки в кэш (30 дней)
                        cache.set(last_sent_key, today, timeout=60 * 60 * 24 * 30)
