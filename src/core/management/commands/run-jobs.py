import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from src.conversion_client.apscheduler import update_currency_conversions, delete_currency_conversions

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py apikey --usage <USAGE> --name <NAME>
    ~~~
    """

    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_currency_conversions,
            trigger=CronTrigger(
                minute=f"*/{settings.MAX_NO_UPDATED_MINS}"
            ),  # https://crontab.guru/
            id="update_currency_conversions",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_currency_conversions,
            trigger=CronTrigger(
                day=f"*/{settings.MAX_STORED_DAYS}"
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
        logger.info("Scheduler shut down successfully!")
