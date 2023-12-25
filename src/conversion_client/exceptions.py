from src.core.exceptions import AppBadRequestException
from django.utils.translation import gettext_lazy as _
from django.conf import settings


CODE_NOT_SUPPORTED_ERROR = 1
TOO_MANY_DAYS_ERROR = 2


class CodeNotSupportedException(AppBadRequestException):
    def __init__(self, code):
        detail = _("{} code not supported").format(code)
        super().__init__(detail, CODE_NOT_SUPPORTED_ERROR)


class TooManyDaysException(AppBadRequestException):
    def __init__(self):
        detail = _("Too many days, maximum is {}").format(
            settings.MAX_STORED_DAYS)
        super().__init__(detail, TOO_MANY_DAYS_ERROR)
