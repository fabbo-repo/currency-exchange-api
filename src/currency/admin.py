from django.contrib import admin
from src.currency.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):

    # This will help disable add functionality
    def has_add_permission(self, request):
        return False

    # This will disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False
