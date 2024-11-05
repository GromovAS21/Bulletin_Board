from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_from_email(subject, message, from_mail, recipient_list):
    """
    Отправка письма
    """

    send_mail(
        subject,
        message,
        from_mail,
        recipient_list,
    )
