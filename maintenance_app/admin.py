from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        "rm_no",
        "ticket_number",  # 👈 custom column
        "name",
        "office",
        "equipment",
        "serial_number",
        "description",
        "priority",
        "created_at",
        "ticket_status",
        "maintenance_type",
        "schedule_category",
    )
    list_filter = (
        "office",
        "equipment",
        "priority",
        "ticket_status",
        "maintenance_type",
        "schedule_category",
    )
    search_fields = ("rm_no", "ticket__ticket_number", "name", "description")
    
     # Hide the ticket field from the add/edit form
    exclude = ("ticket",)

    # 👇 Custom method to show SupportRequest.ticket_number
    def ticket_number(self, obj):
        return obj.ticket.ticket_number if obj.ticket else "-"
    ticket_number.short_description = "Ticket Number"
