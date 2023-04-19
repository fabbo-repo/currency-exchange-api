from conversion.models import Conversion
import json
from conversion.converter import CurrencyConverterService


def create_conversion():
    """
    Create a new Conversion
    """
    Conversion.objects.create(
        conversion_data=json.dumps(
            dict(CurrencyConverterService.get_currency_data().data))
    )
