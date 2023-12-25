import logging
from time import sleep
from django.conf import settings
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from src.conversion_client.models import Conversion
from src.currency.models import Currency

logger = logging.getLogger(__name__)

CURRENCY_CONVERTER_URL = "https://www.xe.com/currencyconverter/convert/"


class CurrencyConversionClient(object):

    def execute_conversions(self, reference_currency_code, ammount=1) -> dict:
        for code in settings.CURRENCY_CODES:
            # Ignore reference_currency_code
            if code == reference_currency_code:
                continue
            requestd_conersion = self.request_conversion(
                reference_currency_code, code
            )
            Conversion.objects.create(
                currency_from=Currency.objects.get(
                    code=reference_currency_code),
                currency_to=Currency.objects.get(code=code),
                conversion_value=requestd_conersion,
            )

    def make_conversions(self, reference_currency_code, ammount=1) -> dict:
        res = {reference_currency_code: ammount}
        for code in settings.CURRENCY_CODES:
            # Ignore reference_currency_code
            if code == reference_currency_code:
                continue
            res[code] = self.make_conversion(
                reference_currency_code, code, ammount
            )
        return res

    def make_conversion(self, currency_from: str, currency_to: str, ammount=1) -> float:
        if currency_from == currency_to:
            return ammount
        now = timezone.now()
        conversions = Conversion.objects.filter(
            currency_from=currency_from,
            currency_to=currency_to,
            created_at__gte=now
            - timezone.timedelta(minutes=settings.MAX_NO_UPDATED_MINS),
        )
        if conversions.exists():
            last_conversion = conversions.last()
            conversion_value = last_conversion.conversion_value
            return conversion_value * ammount
        requestd_conersion = self.request_conversion(
            currency_from, currency_to
        )
        Conversion.objects.create(
            currency_from=Currency.objects.get(code=currency_from),
            currency_to=Currency.objects.get(code=currency_to),
            conversion_value=requestd_conersion,
        )
        return requestd_conersion * ammount

    def delete_conversions(self):
        limit_date = timezone.now() - timezone.timedelta(days=settings.MAX_STORED_DAYS)
        currency_conversions = Conversion.objects.filter(
            created_at__lt=limit_date)
        currency_conversions.delete()

    def request_conversion(self, currency_from, currency_to) -> float:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)

        url = f"{CURRENCY_CONVERTER_URL}?Amount=1&From={currency_from}&To={currency_to}"
        driver.get(url)
        sleep(1)

        result_elements = driver.find_elements(
            by=By.TAG_NAME,
            value="p"
        )

        for element in result_elements:
            if f"1 {currency_from} =" in element.text:
                return float(element.text.split(
                    "=")[-1].replace(currency_to, "").strip())
        return None
