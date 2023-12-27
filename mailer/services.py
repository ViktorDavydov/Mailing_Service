import smtplib

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailer.models import Message, Logs
from datetime import datetime


def send_and_log_mailer(source_form):
    mail_text = Message.objects.get(title=source_form.mail_title).text
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())

    def job_sender():
        try:
            send_mail(
                subject=source_form.mail_title,
                message=mail_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[source_form.client_email]
            )
            logs = Logs(send_name=source_form.send_name, last_try=datetime.now(),
                        status_try='Отправлено')
            logs.save()
        except smtplib.SMTPException as e:
            logs = Logs(send_name=source_form.send_name, last_try=datetime.now(),
                        status_try='Ошибка', server_answer=e)
            logs.save()

    scheduler = BackgroundScheduler()
    conditions = {
        'Ежедневно': 1,
        'Еженедельно': 7,
        'Ежемесячно': 30
    }
    if source_form.send_status == "Создана":
        pass
    elif source_form.send_status == "Завершена":
        scheduler.shutdown()
    else:
        if source_form.send_start > now:
            source_form.send_next_try = source_form.send_start
            for period, period_time in conditions.items():
                if period == source_form.send_period:
                    scheduler.add_job(job_sender, 'interval', minutes=period_time,
                                      start_date=source_form.send_next_try)
                    scheduler.start()
