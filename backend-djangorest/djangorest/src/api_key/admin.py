from django.contrib import admin
from api_key.models import APIKey

@admin.register(APIKey)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'is_active',
    )
    readonly_fields = ('created', 'updated')