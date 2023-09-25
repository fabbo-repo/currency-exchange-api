from rest_framework.test import APITestCase
from rest_framework import status
import logging
import core.tests.utils as test_utils
from django.urls import reverse
from api_key.models import APIKey, ApiUser
from django.conf import settings
from conversion.models import Conversion
from currency.models import Currency
import secrets


class ApiKeyModelTests(APITestCase):
    TEST_ENDPOINT = reverse('currency-get', args=['EUR'])

    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        # Global APIKey for testing purposes
        self.api_key = APIKey.objects.create(
            key=secrets.token_urlsafe(30),
            user=ApiUser.objects.create(username="test"),
            usage_left=3
        )

        # Prepare default data
        settings.CURRENCY_CODES = ["EUR", "USD"]
        settings.MAX_STORED_DAYS = 60
        settings.MAX_NO_UPDATED_MINS = 60
        eur, _ = Currency.objects.get_or_create(code="EUR")
        usd, _ = Currency.objects.get_or_create(code="USD")
        Conversion.objects.get_or_create(
            currency_from=eur,
            currency_to=usd,
            conversion_value=1.0
        )

        return super().setUp()

    def test_usage_left(self):
        """
        Checks API key usage left is decreased
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='APIKey ' + str(self.api_key.key))
        response = test_utils.get(self.client, self.TEST_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_api_key = APIKey.objects.get(key=self.api_key.key)
        self.assertEqual(2, updated_api_key.usage_left)

    def test_no_usage_left(self):
        """
        Checks API key usage left is decreased
        """
        new_api_key = APIKey.objects.create(
            key=secrets.token_urlsafe(30),
            user=ApiUser.objects.create(username="test2"),
            usage_left=0
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='APIKey ' + str(new_api_key.key))
        response = test_utils.get(self.client, self.TEST_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)