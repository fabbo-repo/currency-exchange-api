from django.urls import path
from conversion.api.views import (
    ConversionRetrieveView,
    ConversionDaysListView
)


urlpatterns = [
    path("conversion/days/<int:days>",
         ConversionDaysListView.as_view(), name='conversion-list-by-days'),
    path("conversion/<str:code>", ConversionRetrieveView.as_view(),
         name='conversion-by-code')
]
