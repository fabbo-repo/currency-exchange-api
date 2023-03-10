from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class APIKey(models.Model):
    code = models.UUIDField(
        verbose_name=_("uuid code"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        default=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('API key')
        verbose_name_plural = _('API keys')
        ordering = ['-created']

    def __str__(self) -> str:
        return str(self.code)
