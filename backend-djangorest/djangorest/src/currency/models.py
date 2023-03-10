from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    code = models.CharField(
        verbose_name=_('code'),
        max_length=4,
        primary_key=True
    )

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')
        ordering = ['code']

    def __str__(self) -> str:
        return self.code
