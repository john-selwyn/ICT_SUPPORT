from django.db import models
from django.utils import timezone

class SupportRequest(models.Model):


    UNIT_CHOICES = [
        ("OSDS", "OSDS"),
        ("CID", "CID"),
        ("SGOD", "SGOD"),
        ("BIÑAN ELEMENTARY SCHOOL", "BIÑAN ELEMENTARY SCHOOL"),
        ("CANLALAY ELEMENTARY SCHOOL", "CANLALAY ELEMENTARY SCHOOL"),
        ("PLATERO ELEMENTARY SCHOOL", "PLATERO ELEMENTARY SCHOOL"),
        ("BIÑAN INTEGRATED NATIONAL HIGH SCHOOL", "BIÑAN INTEGRATED NATIONAL HIGH SCHOOL"),
        ("DR. MARCELINO Z. BATISTA MEMORIAL ELEMENTARY SCHOOL", "DR. MARCELINO Z. BATISTA MEMORIAL ELEMENTARY SCHOOL"),
        ("DELA PAZ MAIN ELEMENTARY SCHOOL", "DELA PAZ MAIN ELEMENTARY SCHOOL"),
        ("DELA PAZ WEST ELEMENTARY SCHOOL", "DELA PAZ WEST ELEMENTARY SCHOOL"),
        ("DELA PAZ NATIONAL HIGH SCHOOL", "DELA PAZ NATIONAL HIGH SCHOOL"),
        ("MALABAN ELEMENTARY SCHOOL", "MALABAN ELEMENTARY SCHOOL"),
        ("MALABAN EAST ELEMENTARY SCHOOL", "MALABAN EAST ELEMENTARY SCHOOL"),
        ("NEREO JOAQUIN NATIONAL HIGH SCHOOL", "NEREO JOAQUIN NATIONAL HIGH SCHOOL"),
        ("PAGKAKAISA ELEMENTARY SCHOOL", "PAGKAKAISA ELEMENTARY SCHOOL"),
        ("PEDRO H. ESCUETA MEMORIAL ELEMENTARY SCHOOL", "PEDRO H. ESCUETA MEMORIAL ELEMENTARY SCHOOL"),
        ("ST. ANTHONY INTEGRATED SCHOOL", "ST. ANTHONY INTEGRATED SCHOOL"),
        ("JACOBO Z. GONZALES MEMORIAL NATIONAL HIGH SCHOOL", "JACOBO Z. GONZALES MEMORIAL NATIONAL HIGH SCHOOL"),
        ("BIÑAN CITY SHS ( San Antonio Campus )", "BIÑAN CITY SHS ( San Antonio Campus )"),
        ("SAN VICENTE ELEMENTARY SCHOOL", "SAN VICENTE ELEMENTARY SCHOOL"),
        ("DR. JOSE G. TAMAYO MEMORIAL ELEMENTARY SCHOOL", "DR. JOSE G. TAMAYO MEMORIAL ELEMENTARY SCHOOL"),
        ("TUBIGAN ELEMENTARY SCHOOL", "TUBIGAN ELEMENTARY SCHOOL"),
        ("SAN FRANCISCO ELEMENTARY SCHOOL", "SAN FRANCISCO ELEMENTARY SCHOOL"),
        ("SORO - SORO ELEMENTARY SCHOOL", "SORO - SORO ELEMENTARY SCHOOL"),
        ("ST. FRANCIS INTEGRATED NATIONAL HIGH SCHOOL", "ST. FRANCIS INTEGRATED NATIONAL HIGH SCHOOL"),
        ("BIÑAN CITY SCIENCE AND TECHNOLOGY HIGH SCHOOL", "BIÑAN CITY SCIENCE AND TECHNOLOGY HIGH SCHOOL"),
        ("TOMAS A. TURALBA MEMORIAL ELEMENTARY SCHOOL", "TOMAS A. TURALBA MEMORIAL ELEMENTARY SCHOOL"),
        ("STO. TOMAS ELEMENTARY SCHOOL", "STO. TOMAS ELEMENTARY SCHOOL"),
        ("BIÑAN SECONDARY  SCHOOL OF APPLIED ACADEMIC", "BIÑAN SECONDARY  SCHOOL OF APPLIED ACADEMIC"),
        ("BIÑAN CITY SHS ( STO. TOMAS CAMPUS )", "BIÑAN CITY SHS ( STO. TOMAS CAMPUS )"),
        ("SOUTHVILLE 5A-LANGKIWA ELEM SCHOOL", "SOUTHVILLE 5A-LANGKIWA ELEM SCHOOL"),
        ("LANGKIWA ELEMENTARY SCHOOL", "LANGKIWA ELEMENTARY SCHOOL"),
        ("SOUTHVILLE 5A INTEGRATED NATIONAL HIGH SCHOOL", "SOUTHVILLE 5A INTEGRATED NATIONAL HIGH SCHOOL"),
        ("BIÑAN CITY SHS ( WEST CAMPUS )", "BIÑAN CITY SHS ( WEST CAMPUS )"),
        ("BIÑAN CITY SHS ( TIMBAO CAMPUS )", "BIÑAN CITY SHS ( TIMBAO CAMPUS )"),
        ("LOMA ELEMENTARY SCHOOL", "LOMA ELEMENTARY SCHOOL"),
        ("OUR LADY OF LOURDES ELEMENTARY SCHOOL", "OUR LADY OF LOURDES ELEMENTARY SCHOOL"),
        ("SOUTHVILLE 5-TIMBAO ELEMENTARY SCHOOL", "SOUTHVILLE 5-TIMBAO ELEMENTARY SCHOOL"),
        ("TIMBAO ELEMENTARY SCHOOL", "TIMBAO ELEMENTARY SCHOOL"),
        ("MAMPLASAN ELEMENTARY SCHOOL", "MAMPLASAN ELEMENTARY SCHOOL"),
        ("GANADO ELEMENTARY SCHOOL", "GANADO ELEMENTARY SCHOOL"),
        ("ZAPOTE ELEMENTARY SCHOOL", "ZAPOTE ELEMENTARY SCHOOL"),
        ("MAMPLASAN NATIONAL HIGH SCHOOL", "MAMPLASAN NATIONAL HIGH SCHOOL"),

    ]

    CATEGORY_CHOICES = [
        ("DEPED ACCOUNTS - CREATE", "DEPED ACCOUNTS - CREATE"), 
        ("DEPED ACCOUNTS - RESET", "DEPED ACCOUNTS - RESET"), 
        ("DEPED ACCOUNTS - EXPIRED", "DEPED ACCOUNTS - EXPIRED"),
        ("HARDWARE", "HARDWARE"),
        ("SOFTWARE", "SOFTWARE"),
        ("INTERNET", "INTERNET"),
        ("OTHERS", "OTHERS"),
    ]
    PRIORITY_CHOICES = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
    ]
    STATUS_CHOICES = [
        ("OPEN", "OPEN"),
        ("CLOSED", "CLOSED"),
    ]
    PROCESS_BY_CHOICES = [
        ("RAFAEL AMORANTO", "RAFAEL AMORANTO"),
        ("JACOB BENAVIDIES", "JACOB BENAVIDIES"),
        ("LESTER RAMOS", "LESTER RAMOS"),
        ("SELWYN RANER", "SELWYN RANER"),
        ("MAY VIOLAS", "MAY VIOLAS"),
    ]




    ticket_number = models.CharField(max_length=20, unique=True, primary_key=True, editable=False)  # auto ticket no
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES, default="OSDS")
    email = models.EmailField()
    contact = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="HARDWARE")
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,  default="LOW",editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")
    process = models.CharField(max_length=50, choices=PROCESS_BY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):

        # Generate ticket number if not set
        if not self.ticket_number:
            current_year = timezone.now().year

            # Count how many tickets already exist for this year
            last_ticket = SupportRequest.objects.filter(ticket_number__startswith=str(current_year)) \
                                        .order_by("-ticket_number") \
                                        .first()

            if last_ticket:
                last_seq = int(last_ticket.ticket_number[-3:])  # get last 3 digits
                new_seq = last_seq + 1
            else:
                new_seq = 1

            self.ticket_number = f"{current_year}{new_seq:03d}"  # e.g., 2025001

        # Priority rules mapping
        priority_map = {
            "HARDWARE": "HIGH",
            "INTERNET": "HIGH",
            "SOFTWARE": "MEDIUM",
            "DEPED ACCOUNTS - RESET": "MEDIUM",
            "DEPED ACCOUNTS - EXPIRED": "LOW",
            "DEPED ACCOUNTS - CREATE": "LOW",
            "OTHERS": "LOW",
        }

        # Default to LOW if category not found in map
        self.priority = priority_map.get(self.category, "LOW")

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.ticket_number} {self.name} {self.unit} {self.email} {self.contact} {self.category} {self.description} {self.priority} {self.status} {self.process} {self.created_at}"