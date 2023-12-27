import smtplib

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailer.models import Message, Logs, SendOptions
from datetime import datetime


def send_and_log_mailer(obj_opt, obj_log):
    mail_text = Message.objects.get(title=obj_opt.mail_title).text
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    conditions = {
        'Ежедневно': 1,
        'Еженедельно': 7,
        'Ежемесячно': 30
    }

    def job_sender():
        try:
            send_mail(
                subject=obj_opt.mail_title,
                message=mail_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj_opt.client_email]
            )
            logs = Logs(send_name=obj_opt.send_name,
                        last_try=datetime.now(),
                        status_try='Отправлено', logs_owner=obj_log.request.user)
            logs.save()
        except smtplib.SMTPException as e:
            logs = Logs(send_name=obj_opt.send_name,
                        last_try=datetime.now(),
                        status_try='Ошибка', server_answer=e,
                        logs_owner=obj_log.request.user)
            logs.save()

    scheduler = BackgroundScheduler()

    if obj_opt.send_start > now:
        obj_opt.send_next_try = obj_opt.send_start
        for period, period_time in conditions.items():
            if period == obj_opt.send_period:
                scheduler.add_job(job_sender, 'interval', minutes=period_time,
                                  start_date=obj_opt.send_next_try)
                scheduler.start()
