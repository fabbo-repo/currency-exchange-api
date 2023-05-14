from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.models import AbstractUser


class APIKey(models.Model):
    code = models.UUIDField(
        verbose_name=_("uuid code"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    key = models.CharField(
        verbose_name=_("key"),
        max_length=50,
        default=get_random_secret_key()
    )
    # An usage left of -1 means no limit
    usage_left = models.IntegerField(
        verbose_name=_("usage left"),
        validators=[MinValueValidator(0)],
        default=-1
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


class ApiUser(AbstractUser):
    # Fields to iggnore in db form default User model:
    first_name = None
    last_name = None
    api_key = models.ForeignKey(
        APIKey,
        on_delete=models.DO_NOTHING,
        verbose_name=_("API key"),
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = []
