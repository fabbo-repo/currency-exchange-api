import logging
from django.conf import settings
from django_apscheduler import util
from conversion_client.django_client import get_keycloak_client


logger = logging.getLogger(__name__)


@util.close_old_connections
def update_currency_conversions(max_age=604_800):
    for code in settings.CURRENCY_CODES:
        get_keycloak_client().execute_conversions(code)


@util.close_old_connections
def delete_currency_conversions(max_age=604_800):
    get_keycloak_client().delete_conversions()
