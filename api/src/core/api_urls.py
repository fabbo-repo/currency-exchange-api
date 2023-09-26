from django.urls import path, include
from currency.api import urls as currency_urls
from conversion_client.api import urls as conversion_urls

urlpatterns = [
    # Currency app urls:
    path("", include(currency_urls)),
    # Conversion app urls:
    path("", include(conversion_urls)),
]
