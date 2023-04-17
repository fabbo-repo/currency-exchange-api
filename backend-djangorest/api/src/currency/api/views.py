from currency.models import Currency
from currency.api.serializers import CurrencySerializer
from rest_framework import generics
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from django.views.decorators.vary import vary_on_headers
from api_key.permissions import HasAPIKey


class CurrencyRetrieveView(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    @method_decorator(cache_page(12 * 60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        """
        This view will be cached for 12 hours
        """
        return super(CurrencyRetrieveView, self).get(request, *args, **kwargs)


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    @method_decorator(cache_page(12 * 60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        """
        This view will be cached for 12 hours
        """
        return super(CurrencyListView, self).get(request, *args, **kwargs)
