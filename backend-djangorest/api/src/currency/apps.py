from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class CurrencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currency'

    def ready(self):
        from django.conf import settings
        from currency.models import Currency
        try:
            for currency_code in settings.CURRENCY_CODES:
                _, created = Currency.objects.get_or_create(
                    code=currency_code
                )
                if created:
                    logger.info("Currency code " +
                                currency_code + " created")
        except Exception:
            pass
