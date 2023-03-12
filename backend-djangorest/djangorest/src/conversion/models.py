from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class Conversion(models.Model):
    id = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # Json for conversion data parsed to string
    # To save it:
    # currencyX.conversion_data = json.dumps(data)
    # To retrive it:
    # json.loads(currencyX.conversion_data)
    # Note: Every key and value would have type str
    conversion_data = models.TextField(
        verbose_name=_('data conversion dictionary'),
        default='{}'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Currency conversion')
        verbose_name_plural = _('Currency conversions')
        # Greater to lower date
        ordering = ['-created']

    def __str__(self) -> str:
        return str(self.created)
