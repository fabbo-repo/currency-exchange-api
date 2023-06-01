import logging
import requests
from django.conf import settings
from bs4 import BeautifulSoup
from conversion.models import Conversion
from currency.models import Currency
from django.utils import timezone
from time import sleep

logger = logging.getLogger(__name__)

CURRENCY_CONVERTER_URL = "https://www.xe.com/currencyconverter/convert/"


class CurrencyConversionService:
    def make_conversions(reference_currency_code, ammount=1, is_job=False) -> dict:
        res = {reference_currency_code: ammount}
        for code in settings.CURRENCY_CODES:
            # Ignore reference_currency_code
            if code == reference_currency_code:
                continue
            res[code] = CurrencyConversionService.make_conversion(
                reference_currency_code, code, ammount
            )
            if is_job:
                # Wait half second for next conversion lookup
                sleep(0.5)
        return res

    def make_conversion(currency_from: str, currency_to: str, ammount=1) -> float:
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
        requestd_conersion = CurrencyConversionService._request_conversion(
            currency_from, currency_to, 1
        )
        Conversion.objects.create(
            currency_from=Currency.objects.get(code=currency_from),
            currency_to=Currency.objects.get(code=currency_to),
            conversion_value=requestd_conersion,
        )
        return requestd_conersion * ammount

    def delete_conversions():
        limit_date = timezone.now() - timezone.timedelta(days=settings.MAX_STORED_DAYS)
        currency_conversions = Conversion.objects.filter(
            created_at__lt=limit_date)
        currency_conversions.delete()

    def _request_conversion(currency_from, currency_to, ammount=1) -> float:
        params = {}
        params["Amount"] = ammount
        params["From"] = currency_from
        params["To"] = currency_to
        resp = requests.get(CURRENCY_CONVERTER_URL, params=params)
        try:
            resp.raise_for_status()
        except:
            logger.error("Currency converter connection error")
            raise ConnectionError()
        html = resp.content
        return CurrencyConversionService._filter_html_response(html)

    def _filter_html_response(html) -> float:
        soup = BeautifulSoup(html, "html.parser")
        try:
            return float(soup.body.find_all("p")[2].text.split(" ")[0])
        except:
            logger.error("Html parser no longer valid")
            raise Exception("html parser no longer valid")
