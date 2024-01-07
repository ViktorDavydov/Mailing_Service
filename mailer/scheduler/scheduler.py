from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

from django_apscheduler.jobstores import DjangoJobStore
from mailer.services import job


def set_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    if scheduler.get_job(job_id='send_mail'):
        scheduler.remove_jobstore('mailer_service')

    scheduler.add_jobstore(DjangoJobStore(), 'mailer_service')
    scheduler.add_job(job, trigger=CronTrigger(minute="*/1"), id='send_mail', max_instances=1,
                      jobstore='mailer_service',
                      replace_existing=True)
    scheduler.start()
