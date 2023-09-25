from rest_framework import authentication
from rest_framework import exceptions, authentication
from api_key.models import APIKey
from django.utils.translation import gettext_lazy as _


class ApiKeyAuthentication(authentication.BaseAuthentication):
    def check_api_key(self, api_key_srt: str) -> APIKey | None:
        stored_api_keys = APIKey.objects.filter(is_active=True)
        for stored_key in stored_api_keys:
            if str(stored_key.key) == api_key_srt \
                    and stored_key.usage_left != 0 \
                    and stored_key.is_active:
                return stored_key
        return None

    def get_api_key_srt(self, request) -> str | None:
        """
        Get the access api_key str based on a request.

        Returns None if no authentication details were provided.
        """
        header = authentication.get_authorization_header(request)
        if not header:
            return None
        header = header.decode(authentication.HTTP_HEADER_ENCODING)

        auth = header.split()

        if len(auth) != 2 or auth[0].lower() != "apikey":
            raise exceptions.AuthenticationFailed(_("Unprocessable API key"))
        return auth[1]

    def authenticate(self, request):
        api_key_srt = self.get_api_key_srt(request)

        if not api_key_srt:
            return None

        api_key = self.check_api_key(api_key_srt)

        if not api_key:
            raise exceptions.AuthenticationFailed(_("Invalid API key"))
        elif api_key.user:
            if api_key.usage_left != -1 and api_key.usage_left != 0:
                api_key.usage_left -= 1
                if api_key.usage_left <= 0:
                    api_key.is_active = False
                api_key.save()
                if api_key.is_active:
                    return (api_key.user, None)
            elif api_key.usage_left == -1 and api_key.is_active:
                return (api_key.user, None)
        else:
            exceptions.AuthenticationFailed(
                _("API key without assigned user")
            )

    def authenticate_header(self, request):
        return _("APIKey <api_key>")
