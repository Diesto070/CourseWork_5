import requests

from config import settings


def send_telegram_message(tg_id, message):
    """Функция отправки уведомления в телеграмм."""

    params = {
        "text": message,
        "chat_id": tg_id,
    }
    requests.get(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
