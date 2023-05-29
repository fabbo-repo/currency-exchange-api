from django.conf import settings
from conversion.converter import CurrencyConversionService


def update_currency_conversions():
    for code in settings.CURRENCY_CODES:
        CurrencyConversionService.make_conversions(code)

def delete_currency_conversions():
    CurrencyConversionService.delete_conversions()