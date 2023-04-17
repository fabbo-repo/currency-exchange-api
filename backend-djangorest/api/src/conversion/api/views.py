import json
from conversion.models import Conversion
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from conversion.converter import CurrencyConversionService


class ConversionRetrieveView(APIView):

    def get(self, request, code, format=None):
        if code not in settings.CURRENCY_CODES:
            return Response(
                data={"detail": _("{} code not supported").format(code)},
                status=status.HTTP_400_BAD_REQUEST
            )
        conversions_dict = CurrencyConversionService.make_conversions(code)
        return Response(
            data={
                "code": code,
                "conversions": [
                    {
                        "code": code_to,
                        "value": conversions_dict[code_to]
                    } for code_to in conversions_dict
                ]
            },
        )


class ConversionDaysListView(APIView):

    def get(self, request, days, format=None):
        if days < 1:
            return Response(data=[])
        if days > settings.MAX_STORED_DAYS:
            raise ValidationError(
                detail=_("Too many days, maximum is {}")
                .format(settings.MAX_STORED_DAYS)
            )
        filtered_conversions = Conversion.objects.filter(
            created_at__lte=timezone.now(),
            created_at__gt=timezone.now() - timezone.timedelta(days=days)
        )
        date_ordered_dict = self.conversions_request_to_dict(
            filtered_conversions)
        res = self.conversions_dict_to_response(date_ordered_dict)
        return Response(data=res)

    def conversions_request_to_dict(self, conversions_req) -> dict:
        date_ordered_dict = {}
        for code in settings.CURRENCY_CODES:
            currency_from_conversions = conversions_req.filter(
                currency_from=code
            )
            if currency_from_conversions.exists():
                for conversion in currency_from_conversions:
                    formatted_date = conversion.created_at.strftime("%Y-%m-%d")
                    code_from = code
                    code_to = conversion.currency_to.code
                    value = conversion.conversion_value
                    if formatted_date not in date_ordered_dict:
                        date_ordered_dict[formatted_date] = {
                            code_from: {code_to: value}
                        }
                    else:
                        if code_from not in date_ordered_dict[formatted_date]:
                            date_ordered_dict[formatted_date][code_from] = {
                                code_to: value
                            }
                        else:
                            date_ordered_dict[formatted_date][code_from][code_to] = value
        return date_ordered_dict

    def conversions_dict_to_response(self, conversions_dict: dict) -> dict:
        return {
            "date_conversions": [
                {
                    'conversions': [
                        {
                            "code": code_from,
                            "conversions": [
                                {
                                    "code": code_to,
                                    "value": conversions_dict[date][code_from][code_to]
                                } for code_to in conversions_dict[date][code_from]
                            ]
                        } for code_from in conversions_dict[date]
                    ],
                    'date': date
                } for date in conversions_dict
            ]
        }
