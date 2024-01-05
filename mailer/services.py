import smtplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from mailer.models import Logs, SendOptions
from datetime import datetime, timedelta


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


def set_period(source_form):
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    if source_form.send_period == 'Ежедневно':
        next_try = now + timedelta(days=1)
    elif source_form.send_period == 'Еженедельно':
        next_try = now + timedelta(days=7)
    elif source_form.send_period == 'Ежемесячно':
        next_try = now + timedelta(days=30)
    return next_try


def job():
    mailing_list = SendOptions.objects.all()
    for obj in mailing_list:
        if obj.is_active:
            now = datetime.now()
            now = timezone.make_aware(now, timezone.get_current_timezone())
            if obj.next_try - timedelta(seconds=29) < now < obj.next_try + timedelta(seconds=30):
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
                            obj.next_try = now + timedelta(days=1)
                        elif obj.send_period == 'Еженедельно':
                            obj.next_try = now + timedelta(days=7)
                        elif obj.send_period == 'Ежемесячно':
                            obj.next_try = now + timedelta(days=30)
                        obj.save()
