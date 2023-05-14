from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from api_key.models import APIKey
from django.utils.translation import gettext_lazy as _


class ApiKeyAuthentication(authentication.BaseAuthentication):

    def _check_api_key(self, api_key_key: str) -> APIKey:
        stored_api_keys = APIKey.objects.filter(is_active=True)
        for stored_key in stored_api_keys:
            if str(stored_key.key) == api_key_key \
                    and stored_key.usage_left != 0:
                return stored_key
        return None

    def authenticate(self, request):
        try:
            if 'Authorization' in request.headers:
                authorization = str(request.headers['Authorization'])
                if authorization.lower().startswith("apikey"):
                    api_key = self._check_api_key(
                        request.headers['Authorization']
                        .split(' ')[1])
                    if api_key.user:
                        if api_key.usage_left != -1:
                            api_key.usage_left -= 1
                            api_key.save()
                        return (api_key.user, None)
                    else:
                        exceptions.AuthenticationFailed(
                            _('API key without assigned user'))
        except:
            raise exceptions.AuthenticationFailed(_('Unprocessable API key'))
        raise exceptions.AuthenticationFailed(_('Invalid API key'))

    def authenticate_header(self, request):
        return _("APIKey <api_key>")
