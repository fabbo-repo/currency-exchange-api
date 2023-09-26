from django.contrib import admin
from conversion_client.models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    pass