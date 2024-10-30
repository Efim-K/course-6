import datetime

from mailings.models import Mailings, Attempt
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from smtplib import SMTPException


def send_email(obj):
    """
    Отправка сообщения клиенту
    """
    try:
        send_mail(
            subject=obj.message.message_title,
            message=obj.message.message_text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[obj.email_client],
            fail_silently=False,
        )

        Attempt.objects.create(
            mailing_list=obj, status="Успешно", server_response="Доставлено"
        )

    except SMTPException as e:
        Attempt.objects.create(mailing_list=obj, server_response=f"{e}")


def send_email_period():
    """
    Отправка сообщения клиенту с заданной периодичностью
    """
    datetime_now = datetime.datetime.now(datetime.timezone.utc)

    mailing_list = Mailings.objects.filter(launch_at__lt=datetime_now, is_active=True)

    for mailing in mailing_list:
        mailing.status = "LAUNCHED"

        if mailing.status == "LAUNCHED":
            send_email(mailing)
            if mailing.periodicity == "ONCE":
                mailing.status = "COMPLETED"
                mailing.is_active = False
            if mailing.periodicity == "DAILY":
                mailing.launch_at = datetime_now + datetime.timedelta(days=1)
            if mailing.periodicity == "WEEKLY":
                mailing.launch_at = datetime_now + datetime.timedelta(days=7)
            if mailing.periodicity == "MONTHLY":
                mailing.launch_at = datetime_now + datetime.timedelta(days=30)

        if mailing.completed_at < datetime_now:
            mailing.status = "COMPLETED"
            mailing.is_active = False

        mailing.save(update_fields=["launch_at", "status", "is_active"])
