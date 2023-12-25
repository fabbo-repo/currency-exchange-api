from django.db import models
import uuid
from src.currency.models import Currency
from django.utils.translation import gettext_lazy as _


class Conversion(models.Model):
    id = models.UUIDField(
        verbose_name=_("uuid"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    currency_from = models.ForeignKey(
        Currency,
        verbose_name=_('currency from'),
        related_name="%(app_label)s_%(class)s_from",
        on_delete=models.CASCADE
    )
    currency_to = models.ForeignKey(
        Currency,
        verbose_name=_('currency to'),
        related_name="%(app_label)s_%(class)s_to",
        on_delete=models.CASCADE
    )
    conversion_value = models.FloatField(
        verbose_name=_('conversion value'),
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Currency conversion')
        verbose_name_plural = _('Currency conversions')
        # Greater to lower date
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.created_at)
