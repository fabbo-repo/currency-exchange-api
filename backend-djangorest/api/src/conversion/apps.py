from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class ConversionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversion'

    def ready(self):
        try:
            # Once currency codes are created, then conversions can be fetched
            from conversion.cron import update_currency_conversions
            update_currency_conversions()
        except Exception:
            pass
