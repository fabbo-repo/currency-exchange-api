from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class ApiUser(AbstractUser):
    # Fields to iggnore in db form default User model:
    first_name = None
    last_name = None

    REQUIRED_FIELDS = []


class APIKey(models.Model):
    key = models.CharField(
        verbose_name=_("key"),
        max_length=50,
        unique=True
    )
    # An usage left of -1 means no limit
    usage_left = models.IntegerField(
        verbose_name=_("usage left"),
        validators=[MinValueValidator(0)],
        default=-1
    )
    user = models.ForeignKey(
        ApiUser,
        on_delete=models.DO_NOTHING,
        verbose_name=_("API user")
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
        return str(self.key)
