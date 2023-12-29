import smtplib

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from mailer.models import Logs, SendOptions
from datetime import datetime


def send_and_log_mailer(obj: SendOptions):
    for obj_email in obj.client_email.all():
        try:
            email = EmailMultiAlternatives(
                subject=obj.mail_title.title,
                body=obj.mail_title.text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[obj_email.client_email],
            )
            now = datetime.now()
            now = timezone.make_aware(now, timezone.get_current_timezone())

            email.send()
            Logs.objects.create(
                send_name=obj.mail_title.title,
                last_try=now,
                status_try='Успешно',
                logs_owner=obj.options_owner,
                send_email=obj_email.client_email
            )
        except smtplib.SMTPException as e:
            Logs.objects.create(
                send_name=obj.mail_title.title,
                last_try=now,
                status_try='Ошибка',
                logs_owner=obj.options_owner,
                server_answer=e,
                send_email=obj_email.client_email
            )


def set_period():
    interval = SendOptions.objects.all()
    for obj in interval:
        if obj.send_period == 'Ежедневно':
            obj.interval_try = 1
        elif obj.send_period == 'Еженедельно':
            obj.interval_try = 7
        elif obj.send_period == 'Ежемесячно':
            obj.interval_try = 30
    return obj.interval_try


def job():
    mailing_list = SendOptions.objects.all()
    for obj in mailing_list:
        if obj.is_active:
            now = datetime.now()
            now = timezone.make_aware(now, timezone.get_current_timezone())
            if obj.send_status == 'Создана':
                if obj.send_start <= now:
                    obj.send_start = now
                    obj.send_status = 'Активна'
                    obj.save()
            if obj.send_status == 'Активна':
                if obj.send_finish <= now:
                    obj.send_status = 'Завершена'
                    obj.save()
                elif obj.send_start <= now:
                    send_and_log_mailer(obj)
                    if obj.send_period == 'Ежедневно':
                        obj.interval_try = 1
                    elif obj.send_period == 'Еженедельно':
                        obj.interval_try = 7
                    elif obj.send_period == 'Ежемесячно':
                        obj.interval_try = 30
                    obj.save()


def set_scheduler():
    scheduler = BackgroundScheduler()
    chosen_interval = set_period()
    scheduler.add_job(job, 'interval', days=chosen_interval)
    scheduler.start()
