import json
from conversion.models import Conversion
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ConversionRetrieveView(APIView):

    def get(self, request, code, format=None):
        last_conversion = Conversion.objects.last()
        if last_conversion:
            conversion_data = last_conversion.conversion_data
            json_data = json.loads(conversion_data)
            if code not in json_data:
                return Response(
                    data={"detail": _("{} code not supported").format(code)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                data={
                    "code": code,
                    "conversions": [
                        {
                            "code": conversion,
                            "value": json_data[code][conversion]
                        } for conversion in json_data[code].keys()
                    ]
                },
            )
        return Response(
            data={"detail": _("No conversion data, try later")},
            status=status.HTTP_400_BAD_REQUEST
        )


class ConversionListView(APIView):

    def get(self, request, days, format=None):
        if days < 1:
            return Response(data=[])
        if days > 30:
            days = 30
        data = Conversion.objects.filter(
            created__lte=timezone.now(),
            created__gt=timezone.now() - timezone.timedelta(days=days)
        )
        return Response(
            data={
                "date_conversions": [
                    {
                        'conversions': [
                            {
                                "code": code,
                                "conversions": [
                                    {
                                        "code": conversion,
                                        "value": json.loads(x.conversion_data)[code][conversion]
                                    } for conversion in json.loads(x.conversion_data)[code].keys()
                                ]
                            } for code in json.loads(x.conversion_data).keys()
                        ],
                        'date': x.created.date()
                    } for x in data
                ]
            }
        )
