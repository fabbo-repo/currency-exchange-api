from django.apps import AppConfig
from django.conf import settings
from currency.models import Currency


class CurrencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currency'

    def ready(self):
        for currency_code in settings.CURRENCY_CODES:
            Currency.objects.get_or_create(
                code=currency_code
            )
