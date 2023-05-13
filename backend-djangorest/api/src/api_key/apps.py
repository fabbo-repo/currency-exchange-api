from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class ApiKeyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_key'

    def ready(self):
        from django.conf import settings
        from api_key.models import APIKey
        try:
            if settings.DEFAULT_API_KEY:
                api_key, _ = APIKey.objects.update_or_create(
                    code=settings.DEFAULT_API_KEY,
                    is_active=True
                )
            if not len(APIKey.objects.all()):
                api_key = APIKey.objects.create()
            else:
                api_key = APIKey.objects.filter(is_active=True).last()
            print("#"*40)
            print("API key: " + str(api_key))
            print("#"*40)
        except Exception:
            pass
