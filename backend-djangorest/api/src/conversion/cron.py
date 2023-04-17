from django.conf import settings
from conversion.converter import CurrencyConversionService


def update_currency_conversion():
    for code in settings.CURRENCY_CODES:
        CurrencyConversionService.make_conversions(code)
