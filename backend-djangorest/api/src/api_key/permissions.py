from rest_framework import permissions
from rest_framework.request import Request
from api_key.models import APIKey


class HasAPIKey(permissions.BasePermission):
    message = 'Unauthorized operation'

    def _check_api_key(self, api_key_code: str):
        stored_api_keys = APIKey.objects.filter(is_active=True)
        for stored_key in stored_api_keys:
            if str(stored_key.code) == api_key_code:
                return True
        return False

    def has_permission(self, request: Request, view):
        if 'Authorization' in request.headers:
            authorization = str(request.headers['Authorization'])
            return authorization.startswith("APIKey") \
                and self._check_api_key(request.headers['Authorization']
                                        .split(' ')[1])
        elif 'api_key' in request.query_params.keys():
            return self._check_api_key(request.query_params['api_key'])
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
