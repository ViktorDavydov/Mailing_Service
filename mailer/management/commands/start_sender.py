from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailer.models import SendOptions
from mailer.services import send_and_log_mailer, set_scheduler


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        set_scheduler()
