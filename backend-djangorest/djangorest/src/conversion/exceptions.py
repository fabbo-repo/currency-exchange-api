from django.utils.translation import gettext_lazy as _


class NoCoinConversionException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = _('No coin conversion')
        super().__init__(self.message)


class OldConversionException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = _('Conversion data not updated in the past 24 hours')
        super().__init__(self.message)


class UnsupportedConversionException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = _('No conversion data for the given coin type')
        super().__init__(self.message)


class ConnectionException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'Currency converter connection error'
        super().__init__(self.message)


class HtmlParserException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'Html parser no longer valid'
        super().__init__(self.message)
