from django.urls import path, include
from django.conf import settings
from src.core.swagger import urls as swagger_urls
from src.core import api_urls

handler404 = 'src.core.views.not_found_view'
handler500 = 'src.core.views.error_view'
handler403 = 'src.core.views.permission_denied_view'
handler400 = 'src.core.views.bad_request_view'

urlpatterns = []

# Swagger and documentation will only be available in DEBUG mode
if settings.DEBUG:
    urlpatterns += [
        # Swagger:
        path("api/v1/swagger", include(swagger_urls)),
    ]

urlpatterns += [
    path("api/v1/", include(api_urls)),
]
