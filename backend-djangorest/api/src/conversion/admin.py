from django.contrib import admin
from conversion.models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    pass