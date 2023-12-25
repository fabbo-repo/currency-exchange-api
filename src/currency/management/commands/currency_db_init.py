import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from src.currency.models import Currency

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py currency_db_init
    ~~~
    """

    help = "Init db with currency entries"

    def handle(self, *args, **options):
        for currency_code in settings.CURRENCY_CODES:
            _, created = Currency.objects.get_or_create(
                code=currency_code
            )
            if created:
                logger.info("Currency code " +
                            currency_code + " created")
