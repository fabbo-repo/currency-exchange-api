from django.contrib import admin
from conversion.models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    fields = [
        'conversion_data',
        'created'
    ]
    readonly_fields = [
        'created'
    ]

    # This will help disbale add functionality
    def has_add_permission(self, request):
        return False
