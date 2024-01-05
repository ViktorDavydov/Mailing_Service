from django.apps import AppConfig


class MailerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailer'


class DjangoApschedulerConfig(AppConfig):
    name = "django_apscheduler"
    verbose_name = "Django APScheduler"
