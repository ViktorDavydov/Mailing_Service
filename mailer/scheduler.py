import time

from django.conf import settings
from django.core.mail import send_mail


def job(source):
    send_mail(
        subject=source.mail_title,
        message=source.mail_text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[source.client_email]
    )
