from django.db import models
from django.utils import timezone
from user_support.models import SupportRequest

# === Choices ===
OFFICE_CHOICES = [
    ("OSDS", "OSDS"),
    ("CID", "CID"),
    ("SGOD", "SGOD"),
]

EQUIPMENT_TYPE_CHOICES = [
    ("Desktop", "Desktop"),
    ("Laptop", "Laptop"),
]

PRIORITY_CHOICES = [
    ("LOW", "LOW"),
    ("MEDIUM", "MEDIUM"),
    ("HIGH", "HIGH"),
]

TICKET_STATUS_CHOICES = [
    ("OPEN", "OPEN"),
    ("CLOSED", "CLOSED"),
]

MAINTENANCE_TYPE_CHOICES = [
    ("REPAIR", "REPAIR"),
    ("NON REPAIR", "NON REPAIR"),
]

SCHEDULE_CATEGORY_CHOICES = [
    ("SCHEDULED", "SCHEDULED"),
    ("UNSCHEDULED", "UNSCHEDULED"),
]

# === Priority mapping ===
priority_map = {
    "HARDWARE": "HIGH",
    "INTERNET": "HIGH",
    "SOFTWARE": "MEDIUM",
    "DEPED ACCOUNTS - RESET": "MEDIUM",
    "DEPED ACCOUNTS - EXPIRED": "LOW",
    "DEPED ACCOUNTS - CREATE": "LOW",
    "OTHERS": "LOW",
}

# === Maintenance Model ===
class Maintenance(models.Model):
    rm_no = models.CharField(max_length=50, verbose_name="RM No.", null=True, blank=True)
    ticket = models.OneToOneField(SupportRequest, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    office = models.CharField(max_length=100, choices=OFFICE_CHOICES, null=True, blank=True)
    equipment = models.CharField(max_length=50, choices=EQUIPMENT_TYPE_CHOICES, null=True, blank=True)
    serial_number = models.CharField(max_length=100, verbose_name="Serial Number", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="LOW", editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    ticket_status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, null=True, blank=True)
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES, null=True, blank=True)
    schedule_category = models.CharField(max_length=20, choices=SCHEDULE_CATEGORY_CHOICES, default="UNSCHEDULED")

    def save(self, *args, **kwargs):
        # 🔹 Determine category for mapping
        category = "HARDWARE" if self.equipment else "OTHERS"

        # 🔹 Apply priority rules
        self.priority = priority_map.get(category, "LOW")

        # 🔹 If no linked SupportRequest, create one
        if not self.ticket:
            support_request = SupportRequest.objects.create(
                name=self.name or "Unknown",
                unit=self.office or "OSDS",
                email="noemail@example.com",   # adjust later if Maintenance has email
                contact="N/A",
                category=category,
                description=self.description or "Maintenance request",
                priority=self.priority,        # synced
                status="OPEN"
            )
            self.ticket = support_request
        else:
            # 🔹 If already linked, keep SupportRequest priority in sync
            self.ticket.priority = self.priority
            self.ticket.description = self.description or self.ticket.description
            self.ticket.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rm_no} - {self.ticket} - {self.name} - {self.office} - {self.equipment} - {self.serial_number} - {self.description} - {self.priority} - {self.created_at} - {self.ticket_status} - {self.maintenance_type} - {self.schedule_category}"
