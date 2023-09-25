from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from conversion.apscheduler import update_currency_conversions, delete_currency_conversions

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py apikey --usage <USAGE> --username <USERNAME>
    ~~~
    """

    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_currency_conversions,
            trigger=CronTrigger(
                minute="0",
                hour="*/6"
            ),  # https://crontab.guru/
            id="update_currency_conversions",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_currency_conversions,
            trigger=CronTrigger(
                minute=0,
                hour="*/14"
            ),  # https://crontab.guru/
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            pass
        scheduler.shutdown()
        logger.debug("Scheduler shut down successfully!")
