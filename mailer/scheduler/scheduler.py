from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore
from mailer.services import job


def set_scheduler():
    scheduler = BackgroundScheduler()
    if scheduler.get_job(job_id='send_mail'):
        scheduler.remove_jobstore('mailer_service')
    scheduler.add_jobstore(DjangoJobStore(), 'mailer_service')
    scheduler.add_job(job, 'interval', minutes=1, id='send_mail', jobstore='mailer_service',
                      max_instances=1,
                      replace_existing=True)
    scheduler.start()
