from django.conf import settings
import logging
from conversion.converter import CurrencyConversionService
from django_apscheduler import util


logger = logging.getLogger(__name__)


@util.close_old_connections
def update_currency_conversions(max_age=604_800):
    for code in settings.CURRENCY_CODES:
        CurrencyConversionService.make_conversions(code)


@util.close_old_connections
def delete_currency_conversions(max_age=604_800):
    CurrencyConversionService.delete_conversions()
