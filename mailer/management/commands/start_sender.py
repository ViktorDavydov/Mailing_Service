from django.core.management import BaseCommand

from mailer.scheduler.scheduler import set_scheduler


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        set_scheduler()
