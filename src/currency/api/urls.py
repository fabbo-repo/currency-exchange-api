from django.urls import path
from src.currency.api.views import (
    CurrencyRetrieveView,
    CurrencyListView,
)


urlpatterns = [
    path("currency/<str:pk>", CurrencyRetrieveView.as_view(), name='currency-get'),
    path("currency", CurrencyListView.as_view(), name='currency-list'),
]
