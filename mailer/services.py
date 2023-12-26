from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailer.models import Message
from datetime import datetime


def set_mailer(source_form):
    mail_text = Message.objects.get(title=source_form.mail_title).text

    def job_sender():
        send_mail(
            subject=source_form.mail_title,
            message=mail_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[source_form.client_email],
            fail_silently=True
        )

    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    scheduler = BackgroundScheduler()
    conditions = {
        'Ежедневно': 1,
        'Еженедельно': 7,
        'Ежемесячно': 30
    }
    if source_form.send_start > now:
        source_form.send_next_try = source_form.send_start
        for period, period_time in conditions.items():
            if period == source_form.send_period:
                scheduler.add_job(job_sender, 'interval', minutes=period_time,
                                  start_date=source_form.send_next_try)
                scheduler.start()
