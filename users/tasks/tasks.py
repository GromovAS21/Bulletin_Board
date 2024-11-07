from datetime import datetime
from pathlib import Path
from random import choice

from celery import shared_task

from announcements.tasks import send_mail_from_email
from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def check_birthday_users():
    """
    Проверка дней рождения пользователей и отправка письма с информацией о днях рождения
    """

    current_date = datetime.now().date()
    users = User.objects.filter(date_born=current_date)
    for user in users:
        send_mail_from_email(
            "День рождения!",
            f"Привет, {user.first_name if user.first_name else "Дорогой друг"} ! Сегодня твой день рождения. Поздравляем!",
            EMAIL_HOST_USER,
            [user.email],
        )


@shared_task
def sand_advertising_message():
    """
    Отправка рекламного письма на почту всех пользователей
    """

    with open(Path(__file__).parent.joinpath("advertising_messages.txt"), "r", encoding="utf-8") as file:
        messages = file.read().splitlines()
        message_value = choice(messages)
        users = User.objects.filter(is_active=True)
        for user in users:
            send_mail_from_email(
                "Рекламное письмо",
                message_value,
                EMAIL_HOST_USER,
                [user.email]
            )
