import logging
import requests
from django.conf import settings
from bs4 import BeautifulSoup
from conversion.models import Conversion
from django.utils import timezone
import json

logger = logging.getLogger(__name__)

CURRENCY_CONVERTER_URL = "https://www.xe.com/currencyconverter/convert/"


class CurrencyData:
    def __init__(self, data):
        """Data is a dict with the currency conversions"""
        self.data = data

    def convert(self, currency_from, currency_to, amount: float):
        if currency_from == currency_to:
            return amount
        return float(self.data[currency_from][currency_to]) * amount


class CurrencyConversionService:

    def make_conversions(reference_currency_code, ammount=1):
        res = {
            reference_currency_code: ammount
        }
        for code in settings.CURRENCY_CODES:
            # Ignore reference_currency_code
            if code == reference_currency_code:
                continue
            res[code] = CurrencyConversionService.make_conversion(
                reference_currency_code, code, ammount)
        return res

    def make_conversion(currency_from, currency_to, ammount=1):
        last_conversion = Conversion.objects.last()
        if last_conversion.created > timezone.now() - timezone.timedelta(hours=1):
            return CurrencyConversionService.get_currency_data_from_conversion(last_conversion).convert(currency_from, currency_to, ammount)
        return CurrencyConversionService.request_conversion(currency_from, currency_to, ammount)

    def request_conversion(currency_from, currency_to, ammount=1):
        params = {}
        params["Amount"] = ammount
        params["From"] = currency_from
        params["To"] = currency_to
        resp = requests.get(CURRENCY_CONVERTER_URL, params=params)
        try:
            resp.raise_for_status()
        except:
            logger.error(
                'Currency converter connection error')
            raise ConnectionError()
        html = resp.content
        return CurrencyConversionService.filter_html_response(html)

    def filter_html_response(html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            return float(soup.body.find_all('p')[3].text.split(' ')[3])
        except:
            logger.error('Html parser no longer valid')
            raise Exception('html parser no longer valid')

    def get_currency_data():
        logger.info("Fetching currency data")
        res = {}
        for code in settings.CURRENCY_CODES:
            data = CurrencyConversionService.make_conversions(code)
            data.pop(code)
            res[code] = data
        return CurrencyData(res)

    def get_currency_data_from_json(data):
        return CurrencyData(data)

    def get_currency_data_from_conversion(conversion: Conversion):
        conversion_data = conversion.conversion_data
        data = json.loads(conversion_data)
        return CurrencyData(data)
