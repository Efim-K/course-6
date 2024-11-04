import datetime

from config import settings
from mailings.models import Mailings, Attempt
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from smtplib import SMTPException
from django.core.cache import cache


def send_email(obj):
    """
    Отправка сообщения клиенту
    """
    try:
        send_mail(
            subject=obj.message.message_title,
            message=obj.message.message_text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email.email for email in obj.email_client.all()],
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


def get_total_items_from_cache(name, model):
    """
    Получение списка записей из кеша
    """
    if settings.CACHE_ENABLED:
        key = name
        total_items = cache.get(key)
        if total_items is None:
            total_items = model.objects.all()
            cache.set(key, total_items)
    else:
        total_items = model.objects.all()

    return total_items


def get_total_mailings_active_from_cache():
    """
    Получение общего количества активных рассылок из кеша
    """
    if settings.CACHE_ENABLED:
        key = "mailing_active"
        mailing_active_list = cache.get(key)
        if mailing_active_list is None:
            mailing_active_list = Mailings.objects.filter(status="LAUNCHED")
            cache.set(key, mailing_active_list)
    else:
        mailing_active_list = Mailings.objects.filter(status="LAUNCHED")

    return mailing_active_list
