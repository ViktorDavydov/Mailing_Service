from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailer.models import SendOptions


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pass
