from django.contrib import admin
from .models import SupportRequest

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("ticket_number", "name", "unit", "category", "priority", "status", "created_at",)
    list_filter = ("unit", "category", "priority", "status")
    search_fields = ("ticket_number", "name", "email", "contact")
